@Grab('javax.validation:validation-api:2.0.0.Final')
import groovy.json.JsonOutput
import javax.validation.constraints.NotBlank
import javax.validation.constraints.NotNull
import javax.validation.constraints.Size
import javax.validation.constraints.Pattern

def workspce = env.WORKSPACE

class NodeNpmParams {
    @NotBlank
    String appName
    @NotNull
    @Size(min = 1)
    List<String> team
    String nodeVersion
    String version
    String workingDir
    String dockerfile
    @NotNull
    List<String> buildDestinations // ['ecr1', 'ecr2', 'ecr3']
    @NotNull
    String lintCommand
}

NodeNpmParams pipelineParams

def call(Map params) {
    script {
      pipelineParams = new NodeNpmParams(params)
      pipelineParams.nodeVersion = pipelineParams.nodeVersion ?: '14.x.x'
      pipelineParams.dockerfile = pipelineParams.dockerfile ?: 'Dockerfile'

      assert pipelineParams.lintCommand != null : "** lint command must be set **"
    }

    // Global variables
    String workingDir = pipelineParams.workingDir
    List<String> inputDestinations = pipelineParams.buildDestinations
    String destinationsFound = destinationsResult(inputDestinations)
    String lintCommand = pipelineParams.lintCommand

    pipeline {
        environment {
          AWS_SDK_LOAD_CONFIG = 'true'
          AWS_EC2_METADATA_DISABLED = 'false'
        }

        options {
            disableConcurrentBuilds()
            ansiColor('xterm')
        }

        agent any

        stages {
            stage('Test') {
                steps {
                  script {
                    container('npm') {
                       lint(workingDir, lintCommand)
                    }
                  }
                }
            }

           stage('Docker login') {
             parallel {
              stage ('ECR login') {
               steps {
                  script {
                    container('kaniko') {
                      sh "mkdir -p /kaniko/.docker/"
                      sh """
                      cat <<EOF > /kaniko/.docker/config.json
                      {
                      "credsStore": "ecr-login",
                      "credHelpers": {
                                  "12345678910.dkr.ecr.eu-west-1.amazonaws.com" : "ecr-login"
                              },
                              "auths": {
                                  "https://index.docker.io/v1/": {}
                              }
                      }
                      EOF
                      """
                    }
                  }
               }
              }
             }
           }

           stage('Docker build') {
              steps {
                script {
                  container('kaniko') {
                        sh "/kaniko/executor --context . \
                            --dockerfile ${pipelineParams.workingDir}/${pipelineParams.dockerfile} \
                            --use-new-run \
                            --snapshotMode=redo \
                            ${destinationsFound} "
                  }
                }
              }
           }
        }

        post {
            success {
                echo 'Pipeline Passed'
            }
            failure {
                echo 'Pipeline Failed'
            }
            always {
                echo 'Always'
            }
        }
    }
}

def lint(folder, lintCommand) {
   def lintResult = sh script: """
     set -e
     cd ${folder}
     npm install
     ls -la
     ${lintCommand}
     """,
  returnStatus: true

  if (lintResult != 0) {
    currentBuild.result = 'FAILURE'
    error("Tests Failed")
  }
}

def destinationsResult(destinations) {
  def destinationResult = []

  for (int i = 0; i < destinations.size(); i++) {
     def destination = destinations[i]
     destinationResult << "--destination " + destination
  }

  def destinationResultasString = destinationResult.join(" ")
  return destinationResultasString
}
