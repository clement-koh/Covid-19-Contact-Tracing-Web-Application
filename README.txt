1. After downloading this folder, delete the venv folder
2. In cmd, type the following
    >>> py -3 -m venv venv

3. Activate the virtual environment with the following code
    >>> venv\Scripts\activate

4. Run the following code
    >>> pip install -r requirements.txt
    # Ignore any warning to upgrade pip, or you can upgrade it if you want to, doesn't make a difference

5. Run the following 2 code
    >>> set FLASK_APP=app.py
    >>> flask run


-------------------------------------------------
|	Activate virtual Environment	        	|
-------------------------------------------------
venv\Scripts\activate

-------------------------------------------------
|	Deactivate virtual Environment	        	|
-------------------------------------------------
deactivate

-------------------------------------------------
|	Set Flask to run from app.py            	|
-------------------------------------------------
set FLASK_APP=app.py
flask run