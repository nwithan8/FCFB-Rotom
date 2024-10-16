pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fcfb-rotom'
        CONTAINER_NAME = 'FCFB-Rotom'
        DOCKERFILE = 'Dockerfile'
        CONFIG_JSON = './fcfb/configuration/config.json'
        API_URL = credentials('DEOXYS_API_URL')
        REDDIT_CLIENT_ID = credentials('REDDIT_CLIENT_ID')
        REDDIT_CLIENT_SECRET = credentials('REDDIT_CLIENT_SECRET')
        REDDIT_USERNAME = credentials('REDDIT_USERNAME')
        REDDIT_PASSWORD = credentials('REDDIT_PASSWORD')
        DISCORD_TOKEN = credentials('ROTOM_DISCORD_TOKEN')
        PING_CHANNEL_ID = credentials('ROTOM_CHANNEL_ID')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out the Rotom project...'
                checkout scm
            }
        }
        stage('Get Version') {
            steps {
                script {
                    // Get the latest Git tag
                    def latestTag = sh(script: "git describe --tags --abbrev=0", returnStdout: true).trim()

                    // If there are no tags, default to 1.0.0
                    if (!latestTag) {
                        latestTag = '1.0.0'
                    }

                    // Print the version
                    echo "Current Version: ${latestTag}"

                    // Set the version to an environment variable for use in later stages
                    env.VERSION = latestTag

                    // Set the build description
                    currentBuild.description = "Version: ${env.VERSION}"
                    currentBuild.displayName = "Build #${env.BUILD_NUMBER} - Version: ${env.VERSION}"
                }
            }
        }
        stage('Stop and Remove Existing Bot') {
            steps {
                script {
                    echo 'Stopping and removing the existing Arceus instance...'
                    sh """
                        docker stop ${CONTAINER_NAME} || echo "Rotom is not running."
                        docker rm ${CONTAINER_NAME} || echo "No old Rotom instance to remove."
                    """
                }
            }
        }

        stage('Build') {
            steps {
                echo 'Creating the config.json file...'
                script {
                    def propertiesContent = """
                    {
                        "reddit": {
                            "user_agent": "Rotom Bot ${env.VERSION} by /u/pm_me_cute_sloths_",
                            "client_id": "${env.REDDIT_CLIENT_ID}",
                            "client_secret": "${env.REDDIT_CLIENT_SECRET}",
                            "username": "${env.REDDIT_USERNAME}",
                            "password": "${env.REDDIT_PASSWORD}",
                            "subreddit": "FakeCollegeFootball"
                        },
                        "discord": {
                            "token": "${env.DISCORD_TOKEN}",
                            "ping_channel_id": "${env.PING_CHANNEL_ID}",  // Quote numeric values as well
                            "prefix": "!"
                        },
                        "api": {
                            "url": "${env.API_URL}"
                        }
                    }
                    """.stripIndent()

                    writeFile file: "${env.CONFIG_JSON}", text: propertiesContent
                }

                echo 'Building the Rotom project...'
            }
        }

        stage('Build New Docker Image') {
            steps {
                script {
                    echo 'Building the new Rotom Docker image...'
                    sh """
                        docker build -t ${IMAGE_NAME}:${DOCKERFILE} .
                    """
                }
            }
        }

        stage('Run New Rotom Container') {
            steps {
                script {
                    echo 'Starting the new Rotom container...'
                    sh """
                        docker run -d --restart=always --name ${CONTAINER_NAME} \\
                            --env-file ${CONFIG_JSON} \\
                            ${IMAGE_NAME}:${DOCKERFILE}
                    """
                }
            }
        }

        stage('Cleanup Docker System') {
            steps {
                script {
                    echo 'Pruning unused Docker resources...'
                    sh 'docker system prune -a --force'
                }
            }
        }
    }

    post {
        success {
            echo 'Rotom has been successfully deployed!'
        }
        failure {
            echo 'An error occurred during the Rotom deployment.'
        }
    }
}
