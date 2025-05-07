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

<a name="columns-configuration"></a>

## Columns Configuration

### Columns with Number of Lines Equal to Number of Variables 

These columns have one entry per question/variable:

1. **LIST**: Contains the question text shown to participants. Each line correspond to a question.

2. **TYPES**: Defines the question type (radio, slider, text, etc.). See [question types table](#question-types-table) below for the available types.

   The TYPES column uses a colon-separated format: `questiontype[:option1[:option2[:...]]]`. Adding an `:optional` suffix to the type makes the corresponding question non required.
   > See the [corresponding wiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types) for more information

3. **OPTS**: Contains options for each question type (e.g., radio button choices, slider min/max values). Split by colon (**`:`**) to create choice options. 
    - Values in the OPTS column can include special prefixes like "suff=" or "pref=" to add suffixes or prefixes to Integer, Float and String inputs (add them at the end of the options' list, start by `:` if the OPTS' value is initially empty). 
    - See [OPTS Format and variable values table](#opts-format-and-variable-values-table) below for OPTS format information and examples.

4. **VARS**: Variable names used to store responses in the database. They become field names in the Player model.
    - Variable names should be unique for all Blocpages (two questionnaires may not have same variable name).
    - See [OPTS Format and variable values table](#opts-format-and-variable-values-table) below for information on variables' values for each type.
    - For `radio`, `hradio`, `radiotable`, `radioline`, `checkbox` and `select` types an additional `{variable_name}_strval` variable registers the string representation of the answer.
    - For all types except `info` and `nothing`, an additional `{variable_name}_time` variable registers the time (in seconds) spent on the question.

5. **QUESTTAG**: (Optional) HTML tag to use for question text (default is `h5`).

6. **HASTAGS**: (Optional) Controls whether HTML tags are allowed to format text in questions and options. 1 means True, 0 means False. By default, tags are allowed. In order to show tags « as is » (\<b\>bold\</b\> instead of **bold**), uncomment the column as set the value to 0. If not specified, the last value (or 1 if no values at all) is used

7. **SHOWNUMBERS** (Optional): Whether to show question number before question text (for non randomized questions). 1 means True, 0 means False. Empty lines take last previous value if it is defined, so SHOWNUMBERS may have only one value 1 to number all questions (optionally add 0 on the line where to stop numbering)

#### Columns with Number of Lines Equal to Number of Screens/Pages

These columns have one entry per screen (determined by the BY parameter). Except the required BY column, other columns in this list are optional:

1. **BY**: Defines how many questions to show per screen. Can be a single number or a list of numbers. 0 means all questions in one screen (page).

2. **BY_INTRO**: Text shown at the top of each screen.

3. **MIN_TIMES**: Time in seconds to wait before showing the Next button. Values > 0 enforce waiting time. A value of 0 means no waiting time. Negative values (e.g., -2) mean absolute value minus 1 second (e.g., 1 second) with no auto-scrolling to the top of the page.

4. **PREV_BUTTONS**: Controls whether to show Previous buttons. 1 means True (show), 0 means False (hide).

> Note that and additional `{blocpage}_screen{number}_time` variable is created for each screen in order to tracks the time (in seconds) a user spends on each screen of a Blocpage (unless [NO_SCREEN_TIME column](#no-screen-time-column) is added with a value is set to 1)

#### Columns with Custom Number of Lines

All columns with custom number of lines are optional.

1. **DEPS**: Dependencies between questions. Format is "`dependent_var:controlling_var:value[:inv]`". 
    - The "`inv`" optional suffix makes the dependent question invisible when the condition is not met. Without this suffix the dependent variable only becomes optional when the condition is not met.
    - The number of lines in this column is equal to the number of dependencies in the questionnaire (Blocpage).
    - the "`value`" is the value(s) of the `controlling_var` under which the `dependent_var` becomes required [and visible when the `:inv` suffixe is present]. May contain several values separated by comma (example: `1,2`) or start with `!` which means the opposite of the following value(s) (example: "`!1,3`" means that the `dependent_var` becomes required [and visible] when the `controlling_var` is not equal to 1 or 3).
    > See the [corresponding wiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/4.3-question-dependencies) for more information.

2. **RANDOMORDERS**: Lists of variables to randomize. Can reference user-defined lists or variable names themselves.

3. **RANDOMORDERS_SHOWNUMBERS**: Whether to show question numbers for randomized questions. Array of boolean values (1 for True, 0 for False) corresponding to each RANDOMORDERS entry.

4. **SAME_ORDERS_IN_ALL_ROUNDS**: Whether to use the same randomization across experimental rounds. 1 means True, 0 means False.

##### User-Defined Lists

The optional user-defined lists can be referenced in RANDOMORDERS to randomize their presentation. For example (in leepquest/leepquest.xlsx):

1. **ACTIVITIES_LIST**: a user-defined list containing activity names.

2. **SELF_ESTIM_LIST**: a user-defined list containing self-esteem questions.

These user-defined lists are referenced in the RANDOMORDERS column in the B sheet (blocpage).

To access these lists in code, you can use the format ```getattr(C, blocpage + "_" + list_name)``` or ```C.{blocpage}_{list_name}``` where blocpage is the sheet name where the list is defined.

#### Other Columns 

##### Only one line (valid for the whole Blocpage):

1. **TITLE**: (Optional) Title displayed at the top of the blocpage.

<a name="no-screen-time-column"></a>

2. **NO_SCREEN_TIME**: (Optional) If set to True, disables time tracking for screens.

> Note that the following additional variables are created for each Blocpage:
>  - `{blocpage}_loadtime` to record how long it takes for a Blocpage to load,
> - `{blocpage_name}_nloads` to count how many times a Blocpage has been loaded/reloaded by the user (incremented each time the page is loaded).

##### Columns starting with #:
These are comment columns and are ignored by the system.

#### Notes on Column's Values

- For most columns, if there are fewer values than variables, the last value is used for remaining variables.

- For columns PREV_BUTTONS, SHOWNUMBERS and RANDOMORDERS_SHOWNUMBERS, HASTAGS, NO_SCREEN_TIME a value of 1 means True and 0 means False.

<a name="question-types-table"></a>

## Question Types Table
> | Type | Description | Rendered As | Example Use Case |
> |------|-------------|-------------|------------------|
> | [radio](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#standard-radio-buttons-radio) | Standard radio buttons (vertical) | Vertical radio button group | Single-choice questions with few options |
> | [hradio](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#horizontal-radio-buttons-hradio) | Horizontal radio buttons | Horizontal radio button group | Rating scales, Likert scales |
> | [radioline](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#radio-line-radioline) | Radio buttons in a line with labels | Horizontal scale with labels | Numeric scales (0-5, 1-7) |
> | [radiotable](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#radio-table-radiotable) | Radio buttons in a table | Table with rows as questions, columns as options | Matrix questions with same options |
> | [select](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#select-dropdown-select) | Dropdown menus | Dropdown select menu | Questions with many options |
> | [checkbox](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#checkboxes-checkbox) | Checkbox for boolean responses | Checkbox input | Yes/No questions |
> | [int](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#integer-input-int) | Integer input field | Number input field with validation | Age, count numbers |
> | [float](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#float-input-float) | Decimal number input field | Number input field with decimal support | Precise numeric values |
> | [__slider__](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#slider-question-types) | A slider (integer `slider:int` or float `slider:float`) | Interactive slider with min/max values | Discrete numeric scales / Continuous scales |
> | [stext/string](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#short-text-stextstring) | Single-line text input | Text input field | Short answers |
> | [ltext/longstring](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#long-text-ltextlongstring) | Multi-line text input | Textarea for longer responses | Open-ended questions |
> | [info](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#information-display-info) | Display information (no input) | Text display only | Instructions, explanations |
> | [nothing](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#no-rendering-nothing) | No rendering | Not visible to participants | Skip slots in questionnaire |

<a name='opts-format-and-variable-values-table'></a>
### OPTS Format and Variable Values Table

> | TYPE | OPTS Format | Example OPTS | Variable Value |
> |------|-------------|--------------|----------------|
> | `radio` | List of options | No diploma:Primary education:High School Diploma | __Integer__: 1-n (position of selected option) __String__: Selected option text (in varname_strval) |
> | `hradio` | List of options | Man:Woman:I prefer not to answer | __Integer__: 1-n (position of selected option) __String__: Selected option text (in varname_strval) |
> | `radioline` | Range labels with optional numbers | (very dissatisfied)::::(very satisfied) | __Integer__: Value from range specified in TYPE (e.g., 1-5) __String__: Selected option text (in varname_strval) |
> | `radiotable` (`radiotable:first`, `radiotable`, `radiotable:last`) | List of column headers | Strongly disagree:Somewhat disagree:Somewhat agree:Strongly agree | __Integer__: 1-n (position of selected column) __String__: Selected column text (in varname_strval) |
> | `select` | List of options | France:Abroad | __Integer__: 1-n (position of selected option) __String__: Selected option text (in varname_strval) |
> | `checkbox` | YES:NO or custom labels | YES:NO | __Boolean__: True (1) if checked, False (0) if unchecked __String__: First or second option text based on state (in varname_strval) |
> | `int` | min:max:options | :0:suff=person(s) | __Integer__: Entered integer value |
> | `float` | min:max:step:options | 0:100:0.1:% | __Float__: Entered decimal value |
> | `slider` (`slider:int`, `slider:float`) | min:max:step:options | 0:100:0.1:inv:%:None at all/All income | __Integer__/__Float__: Numeric value selected on slider (depends on TYPE) |
> | `stext` (or `string`) | (No specific format) | Empty or validation hints | String: Entered text |
> | `ltext` (or `longstring`) | (No specific format) | Empty or validation hints | String: Entered text (longer) |
> | `info` | (No input required) | Empty | No value stored (field is just for display) |
> | `nothing` | (Not displayed) | Empty | No variable created |
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
- Group and Subsession variables should be defined inside the corresponding `Group` and `Subsession` classes [as usual in an oTree project](https://otree.readthedocs.io/en/latest/models.html).
    ```python
    class Group(BaseGroup):
         # test_group = models.IntegerField(initial = 1)
        pass
    ``` 
 - Additional Player variables (that aren't defined in the Excel questionnaire definition file) should be defined in the [`PlayerVariables` class](https://deepwiki.com/mxmfrlv/leepquest_otree/3.1-player-variables):
    ```python
    class PlayerVariables:
        # additional player variables should be defined here
        # test = models.IntegerField(initial = 1)
        pass
    ```
 - Use [special `bp_` functions](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#hook-functions) defined in `__init__.py` to dynamically manage blocpages (questionnaires) and questions. In most functions, you may use the `cbp` ('current blocpage') parameter to reference the sheet name in the Excel definition file, or (in `hide_some_bp_quests` and `skip_some_bp_quests` functions) the `var` parameter to reference directly the defined variable.

    > See the deepwiki [Extension Function table](https://deepwiki.com/mxmfrlv/leepquest_otree/1.1-system-architecture#8-extension-points) for a summary.



## More information
https://deepwiki.com/mxmfrlv/leepquest_otree/