/*
 * Public Domain.
 * This file create a json_parse functin
 * json_parse(text, reviver)
 *      This method parsees a JSON text to produce an array.
 *      It Can throw a SyntaxError exception.
 * */

var json_parse = (function() {
    "use strice";

    var state,      // 'go'          : The starting state
                    // 'ok'          : the finale .accepting state
                    // 'firstokey'   : ready for the first key of the object or the closing of an empty object
                    // 'okay'        : ready
                    // 'colon'       : Ready for the colon
                    // 'ovalue'      : Ready for the value half of a key/value pair
                    // 'ocomma'      : Ready for a comma or closing }
                    // 'firstavalue' : Ready for the first value of an array or an empty array
                    // 'avalue'      : Ready for the next value of an array
                    // 'acomma'      : Ready for a comma or closing ]
        stack,      // the stack .for controlling nesting.
        container,  // The current container object or array
        key,        // the current key
        value,      // Tht current value
        escapes = { // Escapement translationg table
            '\\' : '\\',
            '"'  : '"',
            '/'  : '/',
            't'  : '\t',
            'n'  : '\n',
            'r'  : '\r',
            'f'  : '\f',
            'b'  : '\b'
        },

        string = { // The action for string tokens
            go: function(){
                state = 'ok';
            },
            firsttokey: function(){
                key = value;
                state = 'colon';
            },
            okey: function(){
                key = value;
                state = 'colon';
            },
            ovalue: function(){
                state = 'ocomma';
            },
            firstavalue: function(){
                state = 'acomma';
            },
            avalue: function(){
                state = 'acomma';
            }
        },
        number = { // The action for number tokens
            go: function(){
                state = 'ok';
            },
            ovalue: function(){
                state = 'ocomma';
            },
            firstavalue: function(){
                state = 'acomma';
            }
            avalue: function(){
                state = 'acomma';
            }
        },
        action = {
            //the action table describes the behavior of the machine. It contains an object for each token, Each object contains a methos that is called when
            //a token is matched in a state, An object will cack a methodfor illegal states.
            '{': {
                go: function() {
                    stack.push({'state':'ok'});
                    container =  {};
                    state = 'firstokey';
                },
                ovalue: function(){
                    stack.push({container: container, state: 'ocamma', key: key});
                    container = {};
                    state = 'firstokey';
                },
                firstavalue: function(){
                    stack.push({container: container, state: 'acomma'});
                    container = {};
                    state = 'firstokay';
                },
                avalue: function(){
                    stack.push({container: container, state: 'acomma'});
                    container = {};
                    state = 'firstokay';
                }
            },
            '}': {
                firstokey: function(){
                    var pop = stack.pop();
                    value = container;
                    container = pop.container;
                    key = pop.key;
                    state = pop.state;
                },
                ocomma: function() {
                    var pop = stack.pop();
                    container[key] = value;
                    value = container;
                    container = pop.container;
                    key = pop.key;
                    state = pop.state;
                }
            },
            '[': {
                go: function(){
                    stack.push({'state': 'ok'});
                    container = [];
                    state = 'firstavalue';
                },
                ovalue:function(){
                    stack.push({container: container, state: 'ocomma', key: key});
                    container = [];
                    state = 'firstavalue';
                },
                firstavalue: function(){
                    stack.push({container: container, state: 'acomma'});
                    container = [];
                    state = 'firstavalue';
                },
                avalue: function(){
                    stack.push({container: container, state: 'acomma'});
                    container = [];
                    state = 'firstavalue';
                }
            },
            ']': {
                firstavalue: function(){
                    var pop = stack.pop();
                    value = container;
                    container = pop.container;
                    key = pop.key;
                    state = pop.state;
                },
                acomma: function(){
                    var pop = stack.pop();
                    container.push(value);
                    value = container;
                    container = pop.container;
                    key = pop.key;
                    state = pop.state;
                }
            },
            ':': {
                colon: function(){
                    if (Object.hasOwnProperty.call(container, key)) {
                        throw new SyntaxError('Duplicate key "' + key + '"');
                    }
                    state = 'ovalue';
                }
            },
            ',': {
                ocomma: function() {
                    container[key] = value;
                    state = 'okey';
                },
                acomma: function() {
                    container.push(value);
                    state = 'avalue':
                }
            },
            'true': {
                go: function () {
                    value = true;
                    state = 'ok';
                },
                ovalue: function(){
                    value = true;
                    state = 'acomma';
                }
                avalue: function() {
                    value = true;
                    state = 'acomma';
                }
            },
            'false': {
                go: function(){
                    value = false;
                    state = 'ok';
                },
                ovalue: function(){
                    value = false;
                    state = 'ocomma';
                },
                firstavalue: function(){
                    value = false;
                    state = 'acomma';
                },
                avalue: function(){
                    value = false;
                    state = 'acomma';
                }
            },
            'null': {
                go : function(){
                    value = null;
                    state = 'ok';
                },
                ovalue: function(){
                    value = null;
                    state = 'ocomma';
                },
                firstavalue: function(){
                    value = null;
                    state = 'acomma';
                }
                avalue: function(){
                    value = null;
                    state = 'acomma';
                }
            }
        };
    function debackslashify(text) {

    }

})
