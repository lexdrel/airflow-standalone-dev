#!/usr/bin/env python3
import argparse
import subprocess
import os

def init(args):
    BRed='\033[1;31m' 
    URed='\033[4;31m' 
    BPurple='\033[1;35m'      
    BCyan='\033[1;36m'        
    NC='\033[0m' # No Color
    AIRFLOW_HOME = args.AIRFLOW_HOME
    AIRFLOW_VERSION = args.AIRFLOW_VERSION
    PYTHON_VERSION = args.PYTHON_VERSION
    CONSTRAINT_URL = f"https://raw.githubusercontent.com/apache/airflow/constraints-{AIRFLOW_VERSION}/constraints-{PYTHON_VERSION}.txt"
    username = args.username
    firstname = args.firstname
    lastname = args.lastname
    email = args.email
    password = args.password

    if not os.path.exists(AIRFLOW_HOME):
        os.makedirs(AIRFLOW_HOME)

    FULL_AIRFLOW_HOME = os.path.abspath(AIRFLOW_HOME)

    script = f"""
    export AIRFLOW_HOME="{AIRFLOW_HOME}"
    echo 'export AIRFLOW_HOME="{FULL_AIRFLOW_HOME}"' >> ~/.bashrc 
    echo "This CLI command is based on the repo https://github.com/LinkedInLearning/hands-on-introduction-data-engineering-4395021"
    echo "{BRed}Thanks to the LinkedIn Learning Team for the original script{NC}"
    echo "Airflow home is set to: {AIRFLOW_HOME}"

    sleep 3

    echo "Installing Airflow Version $AIRFLOW_VERSION, with Python $PYTHON_VERSION"
    pip install "apache-airflow=={AIRFLOW_VERSION}" --constraint "{CONSTRAINT_URL}"

    echo "Running DB Init"

    airflow db init

    airflow info

    # Give airflow enough time to finish writing it's config files with sleep 5
    sleep 5
    echo "Changing value of {BRed}load_examples{NC} in airflow.cfg to {BPurple}False{NC}"
    sed -i -e '/load_examples =/ s/= .*/= True/' {AIRFLOW_HOME}/airflow.cfg
    echo "Changing value of {BRed}dag_dir_list_interval{NC} in airflow.cfg to {BPurple}2{NC}"
    sed -i -e '/dag_dir_list_interval =/ s/= .*/= 2/' {AIRFLOW_HOME}/airflow.cfg
    echo "Changing value of {BRed}worker_refresh_batch_size{NC} in airflow.cfg  to {BPurple}0{NC}"
    sed -i -e '/worker_refresh_batch_size =/ s/= .*/= 0/' {AIRFLOW_HOME}/airflow.cfg
    echo "Changing value of {BRed}worker_refresh_interval{NC} in airflow.cfg  to {BPurple}0{NC}"
    sed -i -e '/worker_refresh_interval =/ s/= .*/= 0/' {AIRFLOW_HOME}/airflow.cfg
    echo "Changing value of {BRed}workers{NC} in airflow.cfg to {BPurple}2{NC}"
    sed -i -e '/workers =/ s/= .*/= 2/' {AIRFLOW_HOME}/airflow.cfg
    echo "Changing value of {BRed}expose_config{NC} in airflow.cfg to {BPurple}True{NC}"
    sed -i -e '/expose_config =/ s/= .*/= True/' {AIRFLOW_HOME}/airflow.cfg

    # Update CSRF For Webserver
    echo "Changing value of ${BRed}WTF_CSRF_ENABLED${NC} in webserver_config.py to ${BPurple}False${NC}"
    sed -i -e '/WTF_CSRF_ENABLED =/ s/= .*/= False/' ${AIRFLOW_HOME}/webserver_config.py

    # Create User
    airflow users create --username {username} --firstname {firstname} --lastname {lastname} --role Admin --email {email} --password {password}

    echo "${BRed}This has only installed airflow, to run it, you will need to run "lexflow start"${NC}"
    """

    process = subprocess.Popen(['/bin/bash', '-c', script])
    process.communicate()

def newdag(args):
    # Check if AIRFLOW_HOME is set
    airflow_home = os.getenv('AIRFLOW_HOME')
    if not airflow_home:
        print("AIRFLOW_HOME is not set in ~/.bashrc")
        return

    # Check if dag folder exists, if not create it
    dag_folder = os.path.join(airflow_home, 'dags')
    if not os.path.exists(dag_folder):
        os.makedirs(dag_folder)

    # Check if dag_name file exists, if not create it
    dag_name = args.dag_name
    dag_file = f"{os.path.join(dag_folder, dag_name)}.py"
    if os.path.exists(dag_file):
        print(f"Error: File {dag_file} already exists.")
        return

    # Create dag file
    with open(dag_file, 'w') as f:
        f.write(f"""
from datetime import datetime, date
import pandas as pd
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

with DAG(
    dag_id='{dag_name}',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False) as dag:

    def callable_method():
        pass

    # bash_task = BashOperator(
    #     task_id='bash_task',
    #     bash_command='echo bash_task',
    #     dag=dag)
        """)

                # Check if tasks are provided
        if args.tasks:
            tasks = args.tasks.split('>>')
            for task in tasks:
                f.write(f"""
    {task} = PythonOperator(
        task_id='{task}',
        python_callable=callable_method,
        dag=dag)
                """)

        f.write("\n    " + " >> ".join(tasks))

def help(args):
    print("lexflow init --AIRFLOW_HOME /airflow --AIRFLOW_VERSION 2.6.3 --PYTHON_VERSION 3.11 --username admin --firstname Firstname --lastname Lastname --email admin@example.org --password password")
    print("Options:")
    print("  --AIRFLOW_HOME     Specify the airflow home directory (default: ./airflow)")
    print("  --AIRFLOW_VERSION  Specify the airflow version (default: 2.6.3)")
    print("  --PYTHON_VERSION   Specify the python version (default: 3.11)")
    print("  --username         Specify the username (default: admin)")
    print("  --firstname        Specify the firstname (default: Firstname)")
    print("  --lastname         Specify the lastname (default: Lastname)")
    print("  --email            Specify the email (default: admin@example.org)")
    print("  --password         Specify the password (default: password)")

def start(args):
    AIRFLOW_HOME=os.getenv('AIRFLOW_HOME')
    bashCommand = f"""
    export AIRFLOW_HOME="{AIRFLOW_HOME}"
    echo "AIRFLOW_HOME is set to: $AIRFLOW_HOME"

    airflow webserver -D
    airflow scheduler -D
    """
    process = subprocess.Popen(['/bin/bash', '-c', bashCommand])
    process.communicate()

def stop(args):
    bashCommand = f"""
    pkill -f airflow
    """
    process = subprocess.Popen(['/bin/bash', '-c', bashCommand])
    process.communicate()

def main():
    parser = argparse.ArgumentParser(prog='lexflow')
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init')
    absolute_path = os.path.join(os.path.abspath(os.getcwd()), 'airflow')
    init_parser.add_argument('--AIRFLOW_HOME', default=absolute_path)
    init_parser.add_argument('--AIRFLOW_VERSION', default="2.6.3")
    init_parser.add_argument('--PYTHON_VERSION', default="3.11")
    init_parser.add_argument('--username', default="admin")
    init_parser.add_argument('--firstname', default="Firstname")
    init_parser.add_argument('--lastname', default="Lastname")
    init_parser.add_argument('--email', default="admin@example.org")
    init_parser.add_argument('--password', default="password")
    init_parser.set_defaults(func=init)

    help_parser = subparsers.add_parser('help')
    help_parser.set_defaults(func=help)

    start_parser = subparsers.add_parser('start')
    start_parser.set_defaults(func=start)

    stop_parser = subparsers.add_parser('stop')
    stop_parser.set_defaults(func=stop)

    newdag_parser = subparsers.add_parser('newdag')
    newdag_parser.add_argument('--dag_name', required=True)
    newdag_parser.add_argument('--tasks', default="task")
    newdag_parser.set_defaults(func=newdag)


    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()