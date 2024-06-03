
# Contract Red-Lining Utility
Document ingestion tool for replacing context-matched phrases with predefined verbage

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/3.0.x/)
## Run Locally

Clone the project
```bash
git clone https://github.com/jackpots28/redlining.git
```

Go to the project directory
```bash
cd redlining
```

Install dependencies
```bash
python3 -m pip install -r docker_only_requirements.txt
```

Start the flask server
```bash
python3 web_app.py
```

---

## Run via Container

Pull latest image from GitHub Image Registry
```bash
podman pull pull ghcr.io/jackpots28/redlining:latest
```

Create staging directory for output files on local machine
```bash
mkdir /tmp/temp_dir
sudo chmod -R 777 /tmp/temp_dir
```

Run the container - Current entrypoint will not run the Python package but you can interact with the runtime
```bash
podman run -it --rm --entrypoint /usr/bin/bash -p 8080:8080 -v /tmp/temp_dir:/home/devusr/project/output_files ghcr.io/jackpots28/redlining:latest
```

---

## Usage/Examples

From within container runtime
```
(app-root) [devusr@104cf9979ef5 project]$ pwd
/home/devusr/project

# The following show the test of Spire.Doc for Python3 - output to /tmp/temp_dir locally
(app-root) [devusr@104cf9979ef5 project]$ python3 scratch_4.py


user@local_machine:/tmp/temp_dir$ ls -lart
total 28
drwxrwxrwt 13 root   root   12288 Jun  2 17:57 ..
drwxrwxrwx  2 user   user    4096 Jun  2 17:58 .
-rw-r--r--  1  540   root   11241 Jun  2 17:58 ReplaceTextUsingRegexPattern.docx

```


## License

[Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)

