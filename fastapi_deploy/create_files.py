echo # Create main.py > create_files.py
echo import sys >> create_files.py
echo >> create_files.py
echo code = '''from fastapi import FastAPI >> create_files.py
echo >> create_files.py
echo app = FastAPI() >> create_files.py
echo >> create_files.py
echo @app.get(\"/\") >> create_files.py
echo def read_root(): >> create_files.py
echo     return {\"message\": \"Civic Funding API Working!\"} >> create_files.py
echo >> create_files.py
echo @app.get(\"/initiatives\") >> create_files.py
echo def get_initiatives(): >> create_files.py
echo     return [ >> create_files.py
echo         {\"name\": \"Urban Renewal Program\", \"budget\": 1500000}, >> create_files.py
echo         {\"name\": \"Rural Education Initiative\", \"budget\": 800000} >> create_files.py
echo     ] >> create_files.py
echo ''' >> create_files.py
echo >> create_files.py
echo with open('main.py', 'w') as f: >> create_files.py
echo     f.write(code) >> create_files.py
echo print(\"main.py created successfully!\") >> create_files.py