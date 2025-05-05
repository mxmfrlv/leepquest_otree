# Questionnaire tool for otree by Paris Experimental Economics Lab ([LEEP](https://www.parisschoolofeconomics.eu/en/research/research-groups/economics-of-human-behavior/parisian-experimental-economics-laboratory/))

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

4. Open the Excel questionnaire definition file inside your app's folder and modify the questionnaires according to your needs (use the A and B sheets in the `leepquest/leepquest.xlsx` file as example, see the wiki pages [for questionnaire definition](https://deepwiki.com/mxmfrlv/leepquest_otree/2-questionnaire-definition) and [for question types](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types)).
5. If you keep the `B` name for one of your questionnaires make sure to delete or modify the `include_B.html` template used for example.

## Advanced usage
### Templating
To create your own template:

1. Create an HTML file named `include_X.html` in your app's folder, where X is your block name (sheet name inside the questionnaire definition Excel file). If found, the template is included at the top of the page, providing custom introductory content or dynamic logic (via `script` tags).

2. Add your HTML content, using div IDs like `initial_presentation_1`, `initial_presentation_2`, etc. for multi-screen content. For multi-screen questionnaires, only the relevant part of the template is shown based on the current screen number. As the user navigates through screens (using Next/Previous buttons), different parts of the include template become visible.

3. The system will automatically detect and include your template when the corresponding questionnaire block is displayed.

### Integration into complex projects
 - Additional Player variables (that aren't defined in the Excel questionnaire definition file) should be defined in the `PlayerVariables` [class]():
    ```python
    class PlayerVariables:
        # additional player variables should be defined here
        # test = models.IntegerField(initial = 1)
        pass
    ```
- Group and Subsession variables should be defined inside the corresponding `Group` and `Subsession` classes [as usual in an oTree project](https://otree.readthedocs.io/en/latest/models.html).
    ```python
    class Group(BaseGroup):
         # test_group = models.IntegerField(initial = 1)
        pass
    ``` 
 - Use [special `bp` functions](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#hook-functions) defined in `__init__.py` to dynamically manage blocpages (questionnaires) and questions

### Testing with Bots
Add `?participant_label=bot1` (or "bot2" to "bot24", increase the maximum number or add more labels to `bot_labels` in `settings.py`) to the _session-wide-link_ to launch a bot that answers randomly.

## More information
https://deepwiki.com/mxmfrlv/leepquest_otree/