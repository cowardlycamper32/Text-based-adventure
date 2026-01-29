RPGSCRIPT

FUNCS:
    TEXT = TEXT:<name>:<text>
    QUESTION = QUESTION:<name>:<var>:<var_type>:<text>:<option1>,<option2>,...
    IF = IF:<var>:<==|!=|>|<|>=|<=>:<text>:<CMD with different seperator>
    GOTO = GOTO:<line_num>
    VAR = VAR:<var_type>:<var>:<value>
    CLEAR = CLEAR:<var_name>
    RETURN = RETURN:<VARS|text>

    ADD = ADD:<item1>,<item2>,...:<output_var_name>
    SUB = SUB:<item1>,<item2>,...:<output_var_name>
    MUL = MUL:<item1>,<item2>,...:<output_var_name>
    DIV = DIV:<item1>,<item2>:<output_var_name>
    MOD = MOD:<item1>,<item2>:<output_var_name>
    
    //:<comment_text> = a comment (ignored by compiler)

TODO: add POW: x to the power of y
TODO: fuck tetration

$<var_name> references a variable by that name


TYPES:
    STRING = python string
    INT = python integer
    FLOAT = python float
    BOOL = python boolean


TODO: add LOAD: a function for loading external resources, namely jsons, XMLs and .dialogue files


BACKEND:
    variables are stored in a list of dictionaries, specifying variable name and value. possibly gonna have to refactor the VAR system to include type as well