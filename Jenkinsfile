// Jenkinsfile — beginner-friendly declarative pipeline
// Goal: build a simple "Hello World" Docker image and push it to Docker Hub.
//
// Prerequisites (configure once in Jenkins):
//   1. Docker must be installed and available on the Jenkins agent (the `docker` CLI).
//   2. Add a "Username with password" credential in Jenkins with the ID
//      `dockerhub-credentials`, holding your Docker Hub username and a Docker Hub
//      access token (or password).
//
// Tip: change DOCKERHUB_USER below to your own Docker Hub username.

pipeline {
    // Run on any available Jenkins agent.
    agent any

    environment {
        // ----- Edit these values for your own setup -----
        DOCKERHUB_USER = 'aakibgithuber'        // your Docker Hub username
        IMAGE_NAME     = 'hello-world-jenkins'  // name of the image to build
        // ------------------------------------------------

        // Full image reference, e.g. aakibgithuber/hello-world-jenkins
        IMAGE_REF = "${DOCKERHUB_USER}/${IMAGE_NAME}"

        // Load the Docker Hub credentials stored in Jenkins.
        // This creates DOCKERHUB_CREDS_USR (username) and DOCKERHUB_CREDS_PSW (password/token).
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')
    }

    stages {

        // Stage 1: Get the source code from the repository.
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        // Stage 2: Build the Docker image from the Dockerfile.
        // We tag it twice: with the unique Jenkins build number and with `latest`.
        stage('Build Image') {
            steps {
                echo "Building Docker image ${IMAGE_REF}:${BUILD_NUMBER}"
                // The Dockerfile lives in the jenkins-hello-world/ folder.
                dir('jenkins-hello-world') {
                    sh 'docker build -t $IMAGE_REF:$BUILD_NUMBER -t $IMAGE_REF:latest .'
                }
            }
        }

        // Stage 3: Quick sanity check — run the image and print its output.
        stage('Test Image') {
            steps {
                echo 'Running the image to verify it works...'
                sh 'docker run --rm $IMAGE_REF:$BUILD_NUMBER'
            }
        }

        // Stage 4: Log in to Docker Hub using the stored credentials.
        // --password-stdin keeps the password out of the build log.
        stage('Login to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub...'
                sh 'echo "$DOCKERHUB_CREDS_PSW" | docker login -u "$DOCKERHUB_CREDS_USR" --password-stdin'
            }
        }

        // Stage 5: Push both tags to Docker Hub.
        stage('Push Image') {
            steps {
                echo "Pushing ${IMAGE_REF} to Docker Hub..."
                sh 'docker push $IMAGE_REF:$BUILD_NUMBER'
                sh 'docker push $IMAGE_REF:latest'
            }
        }
    }

    // The post section runs after all stages, whether they passed or failed.
    post {
        always {
            echo 'Cleaning up: logging out and removing local images...'
            // Log out and remove local images so the agent stays clean.
            sh 'docker logout || true'
            sh 'docker rmi $IMAGE_REF:$BUILD_NUMBER $IMAGE_REF:latest || true'
        }
        success {
            echo "Success! Pushed ${IMAGE_REF}:${BUILD_NUMBER} and ${IMAGE_REF}:latest"
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above for details.'
        }
    }
}
