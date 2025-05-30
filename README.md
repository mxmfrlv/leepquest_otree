# Questionnaire tool for otree by Paris Experimental Economics Lab ([LEEP](https://www.parisschoolofeconomics.eu/en/research/research-groups/economics-of-human-behavior/parisian-experimental-economics-laboratory/))

A tool for creating questionnaires in oTree using excel sheets. 

Integrates various question types, adapted to different devices (computers or smartphones) with a responsive design.

(See examples in leepquest/leepquest.xlsx)

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Columns Configuration](#columns-configuration)
  - [Columns with Number of Lines Equal to Number of Variables](#columns-with-number-of-lines-equal-to-number-of-variables)
  - [Columns with Number of Lines Equal to Number of Screens/Pages](#columns-with-number-of-lines-equal-to-number-of-screenspages)
  - [Columns with Custom Number of Lines](#columns-with-custom-number-of-lines)
    <!--- [User-Defined Lists](#user-defined-lists) -->
  - [Other Columns](#other-columns)
    - [Only one line (valid for the whole Blocpage)](#only-one-line-valid-for-the-whole-blocpage)
    - [Columns starting with #](#columns-starting-with-)
  - [Notes on Column's Values](#notes-on-columns-values)
- [Question Types Table](#question-types-table)
  - [OPTS format for each type and registered value](#opts-format-for-each-type-and-registered-value)
  - [Slider Question Types](#slider-question-types)
    - [Slider Definition in TYPES](#slider-definition-in-types)
    - [Slider Configuration in OPTS](#slider-configuration-in-opts)
    - [Examples](#examples)
- [Testing with Bots](#testing-with-bots)
- [Advanced usage](#advanced-usage)
  - [Templating](#templating)
  - [Custom validation and custom actions on user's input](#custom-validation-and-custom-actions-on-users-input)
  - [Integration into complex projects](#integration-into-complex-projects)
  - [Questionnaire definition without excel file](#questionnaire-definition-without-excel-file)
- [More information](#more-information)

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
        
    > or use `add_app.py` script instead of `create_app` (`python add_app.py your_app_name`) which will also add your app to the SESSION_CONFIGS in settings.py if it does not already exist.
    
     _If you are sure you'll only need one app (questionnaire) inside your project you may use the original `leepquest` folder as you app's folder. Note that the `create_app` (or `add_app.py`) may not work as expected once the original `leepquest` folder is modified._

4. Open the Excel questionnaire definition file inside your app's folder and modify the questionnaires according to your needs.
    - each sheet in this Excel file represents a questionnaire (which technical name is `Blocpage`),
    - inside each sheet, the questionnaire is configured in columns. See [Columns configuration](#columns-configuration) paragraph below,
    - use the A and B sheets in the `leepquest/leepquest.xlsx` file as example,
    - > for more information see the deepwiki pages [for questionnaire definition](https://deepwiki.com/mxmfrlv/leepquest_otree/2-questionnaire-definition) and [for question types](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types).
5. If you keep the `B` name for one of your questionnaires make sure to delete or modify the `include_B.html` template used for example.

<a name="columns-configuration"></a>

## Columns Configuration

### Columns with Number of Lines Equal to Number of Variables 

These columns have one entry per question/variable:

1. **LIST**: Contains the question text shown to participants. Each line correspond to a question.

2. **TYPES**: Defines the question type (radio, slider, text, etc.). Required for each question. See [question types table](#question-types-table) below for the available types.

   The TYPES column uses a colon-separated format: `questiontype[:option1[:option2[:...]]]`. Adding an `:optional` suffix to the type makes the corresponding question non required.
   > See the [corresponding deepwiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types) for more information

3. **OPTS**: Contains options for each question type (e.g., radio button choices, slider min/max values). Split by colon (**`:`**) to create choice options. 
    - Values in the OPTS column can include special prefixes like "suff=" or "pref=" to add suffixes or prefixes to Integer, Float and String inputs (add them at the end of the options' list, start by `:` if the OPTS' value is initially empty). 
    - See [OPTS format for each type and registered value](#opts-format-for-each-type-and-registered-value) below for OPTS format information and examples.

4. **VARS**: Variable names used to store responses in the database. They become field names in the Player model.
    - Variable names should be unique for all Blocpages (two questionnaires may not have same variable name).
    - See [OPTS format for each type and registered value](#opts-format-for-each-type-and-registered-value) below for information on variables' values for each type.
    - For `radio`, `hradio`, `radiotable`, `radioline`, `checkbox` and `select` types an additional `{variable_name}_strval` variable registers the string representation of the answer.
    <a name="question-time-tracking"></a>
    - For all types except `info` and `nothing`, an additional `{variable_name}_time` variable registers the time (in seconds) spent on the question.
    >Note that a variable name is required for each question in LIST, even for `info` and `nothing` types (for the last one the variable name may not be unique and is not store in the data).

5. **QUESTTAG**: (Optional) HTML tag to use for question text (default is `h5`).

6. **HASTAGS**: (Optional) Controls whether HTML tags are allowed to format text in questions and options. 1 means True, 0 means False. By default, tags are allowed. In order to show tags « as is » (\<b\>bold\</b\> instead of **bold**), uncomment the column as set the value to 0. If not specified, the last value (or 1 if no values at all) is used

7. **SHOWNUMBERS** (Optional): Whether to show question number before question text (for non randomized questions). 1 means True, 0 means False. Empty lines take last previous value if it is defined, so SHOWNUMBERS may have only one value 1 to number all questions (optionally add 0 on the line where to stop numbering)

8. **CONFIRM_BLANK** (Optional): Whether optional questions need a confirmation dialog when leaved empty ("You have not answered all questions. Are you sure to proceed?"). 1 means True, 0 means False. If not specified, the last value (or 0 if no values at all) is used, thus the column may contain only one line with a value of 1 in order to activate confirmation dialog for all optional questions in the questionnaire.



#### Columns with Number of Lines Equal to Number of Screens/Pages

These columns have one entry per screen (determined by the BY parameter). Except the required BY column, other columns in this list are optional:

1. **BY**: Defines how many questions to show per screen. Can be a single number or a list of numbers. 0 means all questions in one screen (page).

2. **BY_INTRO**: Text shown at the top of each screen.

3. **MIN_TIMES**: Time in seconds to wait before showing the Next button. Values > 0 enforce waiting time. A value of 0 means no waiting time. Negative values (e.g., -2) mean absolute value minus 1 second (e.g., 1 second) with no auto-scrolling to the top of the page.

4. **PREV_BUTTONS**: Controls whether to show Previous buttons. 1 means True (show), 0 means False (hide).
<a name="screen-time-tracking"></a>
> Note that and additional `{blocpage}_screen{number}_time` variable is created for each screen in order to tracks the time (in seconds) a user spends on each screen of a Blocpage (unless [NO_SCREEN_TIME](#no-screen-time-column) column is added with a value is set to 1)

#### Columns with Custom Number of Lines

All columns with custom number of lines are optional.

1. **DEPS**: Dependencies between questions. Format is "`dependent_var:controlling_var:value[:inv]`". 
    - The "`inv`" optional suffix makes the dependent question invisible when the condition is not met. Without this suffix the dependent variable only becomes optional when the condition is not met.
    - The number of lines in this column is equal to the number of dependencies in the questionnaire (Blocpage).
    - the "`value`" is the value(s) of the `controlling_var` under which the `dependent_var` becomes required [and visible when the `:inv` suffixe is present]. May contain several values separated by comma (example: `1,2`) or start with `!` which means the opposite of the following value(s) (example: "`!1,3`" means that the `dependent_var` becomes required [and visible] when the `controlling_var` is not equal to 1 or 3).
    > See the [corresponding deepwiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/4.3-question-dependencies) for more information.

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
> | [radioline](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#radio-line-radioline) | Radio buttons in an optionally numbered line with or without labels | Horizontal scale with optional labels | Numeric scales (1-5, 0-7) |
> | [radiotable](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#radio-table-radiotable) | Radio buttons in a table | Table with rows as questions, columns as options | Matrix questions with same options |
> | [select](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#select-dropdown-select) | Dropdown menus | Dropdown select menu | Questions with many options |
> | [checkbox](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#checkboxes-checkbox) | Checkbox for boolean responses | Checkbox input | Yes/No questions |
> | [int](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#integer-input-int) | Integer input field | Number input field with validation | Age, count numbers |
> | [float](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#float-input-float) | Decimal number input field | Number input field with decimal support | Precise numeric values |
> | [__slider__](#slider-question-types) | A slider (integer `slider:int` or float `slider:float`, horizontal [default] of vertical [ by adding `:vertical/HEIGHT` to the type]) | Interactive slider with min/max values | Discrete numeric scales / Continuous scales |
> | [stext/string](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#short-text-stextstring) | Single-line text input | Text input field | Short answers |
> | [ltext/longstring](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#long-text-ltextlongstring) | Multi-line text input | Textarea for longer responses | Open-ended questions |
> | [info](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#information-display-info) | Display information (no input) | Text display only | Instructions, explanations |
> | [nothing](https://deepwiki.com/mxmfrlv/leepquest_otree/2.1-question-types#no-rendering-nothing) | No rendering | Not visible to participants | Skip slots in questionnaire |

<a name='opts-format-for-each-type-and-registered-value'></a>
### OPTS format for each type and registered value

> | TYPE | OPTS Format | Example OPTS | Variable Value |
> |------|-------------|--------------|----------------|
> | `radio` | List of options | `No diploma:Primary education:High School Diploma` | __Integer__: 1-n (position of selected option) __String__: Selected option text (in varname_strval) |
> | `hradio` | List of options | `Man:Woman:I prefer not to answer` | __Integer__: 1-n (position of selected option) __String__: Selected option text (in varname_strval) |
> | `radioline` (`radioline[:min-max][:nonumbers]`) |  Labels to numbers or empty values to show only numbers (or only radio buttons if `:nonumbers` suffixe is added to the type) | `(very dissatisfied)::::(very satisfied)` | __Integer__: Value from range specified in TYPE (e.g., 0-5 for `radioline:0-5` or 1-n by default) __String__: Selected option text (in varname_strval) |
> | `radiotable` (`radiotable:first`, `radiotable`, `radiotable:last`) | List of column headers | `Strongly disagree:Somewhat disagree:Somewhat agree:Strongly agree` | __Integer__: 1-n (position of selected column) __String__: Selected column text (in varname_strval) |
> | `select` | List of options | `France:Abroad` | __Integer__: 1-n (position of selected option) __String__: Selected option text (in varname_strval) |
> | `checkbox` | `YES:NO` or custom labels | `YES:NO` | __Boolean__: True (1) if checked, False (0) if unchecked __String__: First or second option text based on state (in varname_strval) |
> | `int` | `max:min:options` <br>(`max` and `min` may be swapped, `options` include `suff=smth` and/or `pref=smth`) | `100:0:suff=person(s)` | __Integer__: Entered integer value |
> | `float` | `max:min:step:options` <br>(`max` and `min` may be swapped, `options` include `suff=smth` and/or `pref=smth`) | `100:0:0.1:pref=%` | __Float__: Entered decimal value |
> | `slider` (`slider:int` or `slider:float`, with optional `:vertical/HEIGHT`, `:optional`, `:readonly`/`:disabled`) [more info](#slider-definition-in-types)| `max:min:step:options` <br>`max` and `min` may be swapped, `options` are `start_val` (or `inv`), `val pref / val suff` (or just `suff`), `left / right label`, `scale_values/density`, joined by `:` ([more info](#slider-configuration-in-opts)) | `0:100:0.1:inv:%:None at all/All income` <br>[more examples](#examples) | __Integer__/__Float__: Numeric value selected on slider (depends on TYPE) |
> | `stext` (or `string`) | (No specific format) | Empty or prefix/suffix `:pref=@` | String: Entered text |
> | `ltext` (or `longstring`) | (No specific format) | Empty or prefix/suffix `:pref=Comments:suff=(optional)` | String: Entered text (longer) |
> | `info` | (No input required) | Empty | A boolean value True (1) is stored once the field is displayed) |
> | `nothing` | (No input required, not displayed) | Empty | No variable created |

<a name='slider-question-types'></a>
### Slider Question Types

Sliders allow selection of values on a continuous scale. Sliders are implemented using the [nouislider](https://refreshless.com/nouislider/) library and configured through the `TYPES` and `OPTS` columns.

---

#### Slider Definition in `TYPES`

**Format:**  
`slider:type[:orientation/size][:optional]`

- **`type`**: Either `int` or `float`.  
- **`orientation/size`**: Can be `vertical/HEIGHT` (e.g., `vertical/350px`).  
- **`optional`**: Makes the question optional.  

---

#### Slider Configuration in `OPTS`

**Format:**  
`max:min:step[:start_val or inv][:prefix/suffix][:left label/right label][:scale values/density]`

Sliders are configured through a string in `OPTS` with parameters separated by colons. Parameters are defined as follows:

| Parameter Position | Description           | Default | Remarks                                                                 |
|--------------------|-----------------------|---------|---------------------------------------------------------------------------|
| 1 or 2 (`max`)     | Maximum value         | `100`   | The min and max values may be swapped. |
| 2 or 1 (`min`)     | Minimum value         | `0`     |      If `OPTS` contains only one value, it is interpreted as the maximum value, and the slider starts at `0`.                                                                      |
| 3 (`step`)         | Step size             | `1`     |                                                                           |
| 4 (`start_val` or `inv`) | Start value/visibility | `(max+min)/2` | A numeric value sets the slider's start position. Use `inv` to hide the handle initially. Optionally indicate the initial position of the hidden handle: `inv,min` (default, the handle appears from the left upon the first click), `inv,max` (from the right), `inv,mid` or `inv,avg` (from the middle).  <blockquote>Advanced: use [bp_jsvars](#dynamically_set_slider_start_value) to dynamically set the start value</blockquote> |
| 5 (`prefix/suffix`) | Prefix/suffix         | Empty   | Prefix and suffix separated by slash (`prefix/suffix`). Without slash, interpreted as suffix. |
| 6 (`left label/right label`) | Left/right labels | Empty   | Text labels for either side of the slider. Underscores are converted to non-breaking spaces. |
| 7 (`scale values/density`) | Custom scale values/pip density | None | Custom values shown on the slider's scale. Optional density after slash (`/`) controls pip spacing (higher value = more space). |


#### Examples

1. **Question (`LIST`):**  "What percentage of your income do you save?"  
   - **`TYPES`:** `slider:float:optional:vertical/350px`  
   - **`OPTS`:** `0:100:0.1:%:None at all/All:income:0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100/2.5`  

   **Result:**  
   A vertical slider (`350px` height) with values from `0` (bottom) to `100`, step precision `0.1`, and `%` suffix. Labels: "None at all" (left) and "All" (right). Custom scale values every `5` with pip density `2.5`.

2. **Question (`LIST`):** "Do you agree with the sentence above?"  
   - **`TYPES`:** `slider:int`  
   - **`OPTS`:** `100:0:5:inv,mid:$/:Strongly_Disagree/Strongly_Agree`  

   **Result:**  
   A horizontal slider from `0` to `100`, step size `5`, initially hidden handle at midpoint. Values prefixed with `$`. Labels: "Strongly Disagree" (left) and "Strongly Agree" (right).

---
---


## Testing with Bots
Add `?participant_label=bot1` (or "`bot2`" to "`bot24`") to the end of the _session-wide-link_ in order to launch a bot that answers randomly. 

Note that you may increase the maximum number of bots or add more labels to `bot_labels` in `settings.py` (see [bot configuration deepwiki page](https://deepwiki.com/mxmfrlv/leepquest_otree/5-testing-with-bots#bot-configuration)).

## Advanced usage

<a name=templating></a>

### Templating
To create your own template:

1. Create an HTML file named `include_X.html` in your app's folder, where X is your block name (sheet name inside the questionnaire definition Excel file). If found, the template is included at the top of the page, providing custom introductory content or dynamic logic (via `script` tags).

2. Add your HTML content, use div's ID (or class names) `initial_presentation_1`, `initial_presentation_2`, etc. for multi-screen content. For multi-screen questionnaires, only the relevant part of the template is shown based on the current screen number.  A class name `not_initial_presentation_N` may be used to hide the content for the screen `N` only. As the user navigates through screens (using Next/Previous buttons), different parts of the include template become visible.

3. The system will automatically detect and include your template when the corresponding questionnaire block is displayed.

### Custom validation and custom actions on user's input
Inside the `script` tag of the [included template](#templating) it is possible to add custom validation by attributing a function to the `additional_validate` variable in the following way :
```javascript
// Example of custom validation
additional_validate = function(varname){
    if(varname === "email") {
        // Custom email validation
        var value = document.forms[0][varname].value;
        return /^.+@.+\..+$/.test(value);
    }
    return true;
};
```` 
By default, the `additional_validate` variable holds a function which always returns _true_. If this function returns _false_, the field corresponding to the `varname` will be marked as invalid and the user won't be able to proceed to the next screen.

In order to add a custom reaction on user's input it is possible to attribute a function to the `additional_onchange` variable in the following way :
```javascript
// Example of a custom reaction on user's input of a specific field
additional_onchange = function(varname, varvalue){
    // Custom logic when a field changes
    if(varname === "specific_field") {
        // Do something specific for this field using it's current value (varvalue) if necessary
    }
};
```` 
This function is called whenever a form field's value changes and  receives the name of the changed field as its parameter.

### Integration into complex projects

A questionnaire created with the help of this tool can be seamlessly integrated in an otree project by adding the corresponding app name in the `app_sequence` of a session configuration in `SESSION_CONFIGS`. However, for [several reasons](https://deepwiki.com/search/list-me-the-reasons-why-it-wou_22aa1731-667f-4307-bb7f-35e768051f76) (like the need to use one of [included question types](#question-types-table) or integrated [time tracking](https://deepwiki.com/mxmfrlv/leepquest_otree/3.1-player-variables#time-tracking-variables) for [questions](#question-time-tracking) and [screens](#screen-time-tracking)) it could be interesting to use the tool itself to create complex experimental designs other than questionnaires. Note that:

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
 - Use special [`bp_` functions](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#hook-functions) defined in [`__init__.py`](./leepquest/__init__.py#L36-L74) to dynamically manage blocpages (questionnaires) and questions. In most functions, you may use the `cbp` ('current blocpage') parameter to reference the sheet name in the Excel definition file, or (in `hide_some_bp_quests` and `skip_some_bp_quests` functions) the `var` parameter to reference directly the defined variable.

    <!--  > See the deepwiki [Server-side hooks table](https://deepwiki.com/mxmfrlv/leepquest_otree/    3-server-side-components#server-side-hooks) for a brief summary. -->
    Below is a summary of these functions:

    > | Function | Purpose | Default Implementation | Input arguments | Comment |
    > |----------|---------|-----------------------|------------------|---------|
    > | [skip_some_bp_quests](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#skip_some_bp_quests) | Skip specific questions in a blocpage | Returns False | `player`, `cbp`, `n`, `var` | `cbp` is the current blocpage, `n` is the question number, `var` is the question's variable name. Should return True for the question to skip. |
    > | [hide_some_bp_quests](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#hide_some_bp_quests) | Hide specific questions without removing them | Returns False | `player`, `var` | Should return True for the question to hide. See [example of usage](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#hiding-questions-based-on-previous-answers). |
    > | [bp_is_displayed](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#page-display-and-configuration) | Dynamically control whether a blocpage is displayed | Returns True | `player`, `cbp` | Return False to skip the entire Blocpage. See [example of usage](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#conditional-display-of-blocpages). |
    > | [bp_get_timeout_seconds](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#bp_get_timeout_seconds) | Set a timeout for a blocpage | Returns None | `player`, `cbp` | Should return a positive number in seconds to enable timeout. See [example of usage](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#adding-a-timer-to-a-blocpage). |
    > | [bp_get_form_fields](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#bp_get_form_fields) | Add custom fields to a blocpage | Returns empty list | `player`, `cbp` | Should return a list of fields to add (defined in the [`PlayerVariables` class]((https://deepwiki.com/mxmfrlv/leepquest_otree/3.1-player-variables))). See [example of usage](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#extending-the-form-with-custom-fields). |
    > | [bp_vars_for_template](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#bp_vars_for_template) | Add custom variables for the template | Returns empty dict | `player`, `cbp` | Return a dict in a [standard oTree way](https://otree.readthedocs.io/en/latest/pages.html#vars-for-template). See [example of usage](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#adding-custom-template-variables). |
    > | [bp_js_vars](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#bp_js_vars) | Add custom variables for JavaScript | Returns empty dict | `player`, `cbp` | Use in the same way as the [oTree's js_vars function](https://otree.readthedocs.io/en/latest/templates.html#passing-data-from-python-to-javascript-js-vars). <a name="dynamically_set_slider_start_value" id="dynamically_set_slider_start_value"></a>In order to dynamically set a slider's starting values add the "slider_starts" key containing a dict with sliders' variable names as keys with corresponding starting values.  |
    > | [bp_before_next_page](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#lifecycle-hooks). | Execute code before moving to next page | Does nothing | `player`, `timeout_happened`, `cbp`, `next_cbp` |  `next_cbp` is the next blocpage's name. |
    > | [bp_live_event](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#live-interaction) | Handle custom live events | Returns None | `player`, `cbp`, `data` | The data sent and returned should be in string format and prefixed by "custom\|". On client side, use liveSend(\`custom\|${data}\`) to send the data and [`customLiveRecv`](https://deepwiki.com/mxmfrlv/leepquest_otree/7.2-client-api#3-object-object) function to treat the received data. See [example of usage](https://deepwiki.com/mxmfrlv/leepquest_otree/7.1-server-api#handling-custom-live-events) |

### Questionnaire definition without excel file

This tool normally uses an Excel file to define questionnaires, but it also provides an alternative way to define questionnaires directly in code using a `CUSTOM_LQ_C` class when you don't want to use an Excel file. To use a `CUSTOM_LQ_C` class in your `__init__.py` file, you need to:

1. Define the `CUSTOM_LQ_C` class in your `__init__.py` file **before** the `PlayerVariables` class.
2. Structure the class to include all the necessary attributes that would normally come from the Excel file. Add the following attributes:
   - `BLOCPAGES`: List of blocpage names (sections of your questionnaire)
   - `TRACK_BLOCPAGE_LOADS`: Usually the same as `BLOCPAGES`, used for tracking page loads
   - For each blocpage, define the attributes corresponding to the [columns in excel sheets](#columns-configuration), adding to each of them a prefix of the blocpage's name followed by an underscore.  
     E.g., for the `"X"` blocpage, you could define:
     1. `X_LIST`: The question texts
     2. `X_TYPES`: The [question types](#question-types-table) (`radioline`, `slider`, `select`, etc.)
     3. `X_OPTS`: The [options](#opts-format-for-each-type-and-registered-value) for each question
     4. `X_VARS`: The variable names to store responses
     5. `X_BY`: How many questions to show per screen (**may only be a positive number**)
     6. `X_TITLE`: The title of the blocpage
3. Make sure the Excel file (file named `leepquest.xlsx` or `[APP_NAME].xlsx`) doesn't exist in your app directory. The system will only use your `CUSTOM_LQ_C` class if it can't find the Excel file.

 Example of CUSTOM_LQ_C implementation:

```python
# Define CUSTOM_LQ_C class (just above the PlayerVariables class)
class CUSTOM_LQ_C:  
    BLOCPAGES = ["A", "B"]  
    TRACK_BLOCPAGE_LOADS = ["A", "B"]  

    # Blocpage A: Demographics  
    A_LIST = ["How old are you?", "What is your gender?", "What is your country of birth?"]  
    A_TYPES = [["slider", "int"], ["hradio"], ["select"]]  
    A_OPTS = [["99", "18", "1", "18"], ["Man", "Woman", "Other"], ["France", "USA", "Other"]]  
    A_VARS = ["age", "gender", "country"]  
    A_BY = 3  
    A_BY_INTRO = ["Demographics"]  
    A_TITLE = "Demographics"  

    # Blocpage B: Survey Questions  
    B_LIST = [  
        "Do you agree with statement 1?",  
        "Do you agree with statement 2?",  
        "Do you agree with statement 3?"  
    ]  
    B_TYPES = [["radio"]]*3
    B_OPTS = [  
        ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],   
    ]*3 
    B_VARS = ["q1", "q2", "q3"]  
    B_BY = 1  
    B_BY_INTRO = ["Survey Questions"]  
    B_TITLE = "Survey Questions"  
```

## More information
https://deepwiki.com/mxmfrlv/leepquest_otree/