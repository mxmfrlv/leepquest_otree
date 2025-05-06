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

    ) and add your app to SESSION_CONFIGS in `settings.py`
        
    - or use `add_app.py` script instead of `create_app` (`python add_app.py your_app_name`) which will also add your app to the SESSION_CONFIGS in settings.py if it does not already exist.
    
     _If you are sure you'll only need one app (questionnaire) inside your project you may use the original `leepquest` folder as you app's folder. Note that the `create_app` (or `add_app.py`) may not work as expected once the original `leepquest` folder is modified._

4. Open the Excel questionnaire definition file inside your app's folder and modify the questionnaires according to your needs.
    - each sheet in this Excel file represents a questionnaire (which technical name is `Blocpage`),
    - inside each sheet, the questionnaire is configured in columns. See [Columns configuration](#columns-configuration) paragraph below,
    - use the A and B sheets in the `leepquest/leepquest.xlsx` file as example,
    - also  see the deepwiki pages [for questionnaire definition](https://deepwiki.com/mxmfrlv/leepquest_otree/2-questionnaire-definition) and [for question types](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types).
5. If you keep the `B` name for one of your questionnaires make sure to delete or modify the `include_B.html` template used for example.

<a id="columns-configuration"></a>

## Columns Configuration

### Columns with Number of Lines Equal to Number of Variables 

These columns have one entry per question/variable:

1. **LIST**: Contains the question text shown to participants. Each line correspond to a question.

2. **TYPES**: Defines the question type (radio, slider, text, etc.). The following types are available :

    >    | Type | Description | Example Use Case |
    >    |------|-------------|------------------|
    >    | radio | Standard radio buttons (vertical) | Single-choice questions with few options |
    >    | hradio | Horizontal radio buttons | Rating scales, Likert scales |
    >    | radioline | Radio buttons in a line with labels | Numeric scales (0-5, 1-7) |
    >    | radiotable | Radio buttons in a table | Matrix questions with same options |
    >    | checkbox | Checkbox for boolean responses | Yes/No questions |
    >    | select | Dropdown menus | Questions with many options |
    >    | slider | A slider (integer `slider:int` or float `slider:float`) | Discrete numeric scales / Continuous scales  
    >    | ltext/longstring | Multi-line text input | Open-ended questions |
    >    | stext/string | Single-line text input | Short answers |
    >    | int | Integer input field | Age, count numbers |
    >    | float | Decimal number input field | Precise numeric values |
    >    | info | Display information (no input) | Instructions, explanations |
    >    | nothing | No rendering | Skip slots in questionnaire |

   The TYPES column uses a colon-separated format: `questiontype[:option1[:option2[:...]]]`. Adding an `:optional` suffix to the type makes the corresponding question non required.
   > See the [corresponding wiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types) for more information

3. **OPTS**: Contains options for each question type (e.g., radio button choices, slider min/max values). Split by colon (**`:`**) to create choice options. Values in the OPTS column can include special prefixes like "suff=" or "pref=" to add suffixes or prefixes to inputs.

4. **VARS**: Variable names used to store responses in the database. They become field names in the Player model.

5. **QUESTTAG**: (Optional) HTML tag to use for question text (default is `h5`).

6. **HASTAGS**: (Optional) Controls whether HTML tags are allowed to format text in questions and options. 1 means True, 0 means False. By default, tags are allowed. In order to show tags « as is » (\<b\>bold\</b\> instead of **bold**), uncomment the column as set the value to 0. If not specified, the last value (or 1 if no values at all) is used

7. **SHOWNUMBERS** (Optional): Whether to show question number before question text (for non randomized questions). 1 means True, 0 means False. Empty lines take last previous value if it is defined, so SHOWNUMBERS may have only one value 1 to number all questions (optionally add 0 on the line where to stop numbering)

### Columns with Number of Lines Equal to Number of Screens/Pages

These columns have one entry per screen (determined by the BY parameter). Except the required BY column, other columns in this list are optional:

1. **BY**: Defines how many questions to show per screen. Can be a single number or a list of numbers. 0 means all questions in one screen (page).

2. **BY_INTRO**: Text shown at the top of each screen.

3. **MIN_TIMES**: Time in seconds to wait before showing the Next button. Values > 0 enforce waiting time. A value of 0 means no waiting time. Negative values (e.g., -2) mean absolute value minus 1 second (e.g., 1 second) with no auto-scrolling to the top of the page.

4. **PREV_BUTTONS**: Controls whether to show Previous buttons. 1 means True (show), 0 means False (hide).

### Columns with Custom Number of Lines

All columns with custom number of lines are optional.

1. **DEPS**: Dependencies between questions. Format is "`dependent_var:controlling_var:value[:inv]`". 
    - The "`inv`" optional suffix makes the dependent question invisible when the condition is not met. Without this suffix the dependent variable only becomes optional when the condition is not met.
    - The number of lines in this column is equal to the number of dependencies in the questionnaire (Blocpage).
    - the "`value`" is the value(s) of the `controlling_var` under which the `dependent_var` becomes required [and visible when the `:inv` suffixe is present]. May contain several values separated by comma (example: `1,2`) or start with `!` which means the opposite of the following value(s) (example: "`!1,3`" means that the `dependent_var` becomes required [and visible] when the `controlling_var` is not equal to 1 or 3).
    - See the [corresponding wiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/4.3-question-dependencies) for more information.

2. **RANDOMORDERS**: Lists of variables to randomize. Can reference user-defined lists or variable names themselves.

3. **RANDOMORDERS_SHOWNUMBERS**: Whether to show question numbers for randomized questions. Array of boolean values (1 for True, 0 for False) corresponding to each RANDOMORDERS entry.

4. **SAME_ORDERS_IN_ALL_ROUNDS**: Whether to use the same randomization across experimental rounds. 1 means True, 0 means False.

#### User-Defined Lists

The optional user-defined lists can be referenced in RANDOMORDERS to randomize their presentation. For example (in leepquest/leepquest.xlsx):

1. **ACTIVITIES_LIST**: a user-defined list containing activity names.

2. **SELF_ESTIM_LIST**: a user-defined list containing self-esteem questions.

These user-defined lists are referenced in the RANDOMORDERS column in the B sheet (blocpage).

To access these lists in code, you can use the format ```getattr(C, blocpage + "_" + list_name)``` or ```C.{blocpage}_{list_name}``` where blocpage is the sheet name where the list is defined.

### Other Columns 

#### Only one line:

1. **TITLE**: (Optional) Title displayed at the top of the blocpage.

2. **NO_SCREEN_TIME**: (Optional) If set to True, disables time tracking for screens.

#### Columns starting with #:
These are comment columns and are ignored by the system.

### Notes on Column's Values

- For most columns, if there are fewer values than variables, the last value is used for remaining variables.

- For columns like MIN_TIMES, PREV_BUTTONS, SHOWNUMBERS and RANDOMORDERS_SHOWNUMBERS, a value of 1 means True and 0 means False.

---

## Testing with Bots
Add `?participant_label=bot1` (or "`bot2`" to "`bot24`") to the end of the _session-wide-link_ in order to launch a bot that answers randomly. 

Note that you may increase the maximum number of bots or add more labels to `bot_labels` in `settings.py` (see [bot configuration deepwiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/5-testing-with-bots#bot-configuration)).

## Advanced usage
### Templating
To create your own template:

1. Create an HTML file named `include_X.html` in your app's folder, where X is your block name (sheet name inside the questionnaire definition Excel file). If found, the template is included at the top of the page, providing custom introductory content or dynamic logic (via `script` tags).

2. Add your HTML content, using div IDs like `initial_presentation_1`, `initial_presentation_2`, etc. for multi-screen content. For multi-screen questionnaires, only the relevant part of the template is shown based on the current screen number. As the user navigates through screens (using Next/Previous buttons), different parts of the include template become visible.

3. The system will automatically detect and include your template when the corresponding questionnaire block is displayed.

### Integration into complex projects
 - Additional Player variables (that aren't defined in the Excel questionnaire definition file) should be defined in the [`PlayerVariables` class](https://deepwiki.com/mxmfrlv/leepquest_otree/3.1-player-variables):
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
 - Use [special `bp` functions](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#hook-functions) defined in `__init__.py` to dynamically manage blocpages (questionnaires) and questions. In most functions, you may use the `cbp` ('current blocpage') parameter to reference the sheet name in the Excel definition file, or (in `hide_some_bp_quests` and `skip_some_bp_quests` functions) the `var` parameter to reference directly the defined variable.



## More information
https://deepwiki.com/mxmfrlv/leepquest_otree/