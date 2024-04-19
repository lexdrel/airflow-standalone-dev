# Lexflow: Your Airflow Docker Solution by Lexdrel
Welcome to Lexflow, a comprehensive Docker solution designed to streamline your data pipeline management. This project provides a Docker image pre-loaded with Apache Airflow, Pandas, and a custom Command Line Interface (CLI) to simplify your data engineering tasks.

## Key Features
- Apache Airflow: An open-source platform to programmatically author, schedule and monitor workflows. With Airflow pre-installed, you can manage complex pipelines with ease.
- Pandas: A powerful data manipulation library for Python. With Pandas, you can perform efficient data analysis within the same environment.
- Custom CLI: Our custom CLI provides a user-friendly interface to manage your workflows. You can start, stop, and even generate Directed Acyclic Graphs (DAGs) with simple commands.

## Requisites
To use Lexflow, you need the following prerequisites:
- Docker: Install Docker on your machine. You can download it from the official Docker website.
- Visual Studio Code (VSCode): Install VSCode, a popular code editor, for a better development experience. You can download it from the official VSCode website.

## Getting Started
Lexflow is a command-line interface (CLI) tool that provides various functionalities. Here's how to use it:

### Initialization
To initialize Lexflow, use the init command. This command accepts several optional arguments:

```console
lexflow init --AIRFLOW_HOME=<path> --AIRFLOW_VERSION=<version> --PYTHON_VERSION=<version> --username=<username> --firstname=<firstname> --lastname=<lastname> --email=<email> --password=<password>
```
--AIRFLOW_HOME: The home directory for Airflow. Defaults to the current directory appended with '/airflow'.
--AIRFLOW_VERSION: The version of Airflow to use. Defaults to '2.6.3'.
--PYTHON_VERSION: The version of Python to use. Defaults to '3.11'.
--username: The username for the admin user. Defaults to 'admin'.
--firstname: The first name of the admin user. Defaults to 'Firstname'.
--lastname: The last name of the admin user. Defaults to 'Lastname'.
--email: The email of the admin user. Defaults to 'admin@example.org'.
--password: The password for the admin user. Defaults to 'password'.

### Help
To get help on using Lexflow, use the help command:
```console
lexflow help
```

### Start
To start Airflow with the lexflow init configuration, use the start command:
```console
lexflow start
```

### Stop
To stop Lexflow, use the stop command:
```console
lexflow stop
```

### Create a New DAG
To create a new Directed Acyclic Graph (DAG), use the newdag command. This command requires the --dag_name argument and accepts an optional --tasks argument:

```console
lexflow newdag --dag_name=<dag_name> --tasks=<tasks>
```

--dag_name: The name of the new DAG. This argument is required.
--tasks: The tasks for the new DAG. Defaults to 'task', or you can use 'task1>>task2>>task3' to create 3 tasks inside the dag file

## Implementating this image to you docker image or devcontainer
### Dockerimage
```console
FROM lexdrel/airflow-2.6.3-python-3.11

# This will set the airflow folder
RUN export AIRFLOW_HOME=\"${PWD#$HOME/}/airflow\"' >> ~/.bashrc

# your custom docker procedure
```

### devcontainer
Inside a devcontainer.json copy and paste this code:
```console
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
{
	"name": "Airflow Standalone",
	// Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
	"image": "lexdrel/airflow-2.6.3-python-3.11",
	"customizations": {
		"vscode": {
			"extensions": [
				"GitHub.github-vscode-theme",
				"alexcvzz.vscode-sqlite",
				"ms-python.python"
			]
		}
	},

	// Features to add to the dev container. More info: https://containers.dev/features.
	// "features": {},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// "forwardPorts": [],

	// Use 'postCreateCommand' to run commands after the container is created.
	"postCreateCommand": "echo 'export AIRFLOW_HOME=\"${PWD#$HOME/}/airflow\"' >> ~/.bashrc"

	// Configure tool-specific properties.
	// "customizations": {},

	// Uncomment to connect as root instead. More info: https://aka.ms/dev-containers-non-root.
	// "remoteUser": "root"
}
```