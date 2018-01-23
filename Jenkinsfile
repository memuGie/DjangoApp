node() {
    stage('Checkout') {
        checkout scm
        sh 'echo $BRANCH_NAME'
    }

    stage('Build project') {
    }

    stage('Run UT') {
        sh 'pwd'
    }

    if (env.BRANCH_NAME == 'master') {
        stage('Deploy') {
            sh 'ls -la'
        }
    }
}