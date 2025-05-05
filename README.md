# Questionnaire tool for otree by Paris Experimental Economics Lab ([LEEP](https://www.parisschoolofeconomics.eu/en/research/pse-research-centers/leep-experimental-economics-lab/))

A tool for creating questionnaires in oTree using excel sheets. See examples in leepquest/leepquest.xlsx

## Requirements
[oTree](http://otree.org/) v5+, [pandas](https://pypi.org/project/pandas/), [openpyxl](https://pypi.org/project/openpyxl/) (`pip install -U otree pandas openpyxl`).

## Usage
1. Clone this repository or download the files
2. Make sure you have all required dependencies installed
3. [Recommended] Launch `create_app` script providing the new app's name (this script will:
   - copy the `leepquest` folder giving the provided app's name to the new folder, 
   - change the NAME_IN_URL parameter inside the `__init__.py` file inside the new folder and
   - change the name of the Excel questionaire definition file (`leepquest.xlsx`) with the provided app's name [note that this is optional, if the `leepquest.xlsx` file is present inside the folder, it will be used instead]

    ) and add your app to SESSION_CONFIGS in `settings.py`:
        
    - or use `add_app.py` script instead of `create_app` (`python add_app.py your_app_name`) which will also add your app to the SESSION_CONFIGS in settings.py if it does not already exist.
    
     _If you are sure you'll only need one app (questionnaire) inside your project you may use the original `leepquest` folder as you app's folder. Note that the `create_app` may not work as expected once the original `leepquest` folder is modified._

4. Open the Excel questionnaire definition file inside your app's folder and modify the questionnaires according to your needs (see the [corresponding wiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/2-questionnaire-definition)).
5. If you keep the `B` name for one of your questionnaires make sure to delete or modify the `include_B.html` template used for example.



## More information
https://deepwiki.com/mxmfrlv/leepquest_otree/