#define URL_BASE       http://easyCurl.com/test/objs
#define URL            '<<URL_BASE>>'
#define URL_OBJ01      '<<URL_BASE>>/myObj01'
#define URL_OBJ02      '<<URL_BASE>>/myObj02'

#define METHOD_POST    'POST'
#define METHOD_GET     'GET'
#define METHOD_DELETE  'DELETE'
#define METHOD_PUT     'PUT'

#define HEADER_CONTENT_TYPE 'Content-Type: application/json;charset=UTF-8'
#define HEADER_ACCEPT       'Accept: application/json'

#define BODY_POST_OBJ01     '{"id":"myObj","description":" the obj created for testing purpose","version":"0.0.1","validity":true}'
#define BODY_PUT_OBJ02      '{"description":" the second obj created for testing purpose","version":"0.0.1","validity":true}'
#define BODY_EMPTY          ''

#define TC_GET_NULL () \
- TC_GET_NULL: \
    RESTCASES: \
        - URL: <<URL>>\
          METHOD: <<METHOD_GET>>\
          HEADERS: [<<HEADER_CONTENT_TYPE>>, <<HEADER_ACCEPT>>]\
          BODY: <<BODY_EMPTY>>\
    CONTROL: 'LOOP:2, DELAY:1'\

#define TC_CREATE_DELETE () \
- TC_CREATE_DELETE: \
    RESTCASES: \
        - URL: <<URL>>\
          METHOD: <<METHOD_POST>>\
          HEADERS: [<<HEADER_CONTENT_TYPE>>, <<HEADER_ACCEPT>>]\
          BODY: <<BODY_POST_OBJ01>>\
\
        - URL: <<URL_OBJ01>>\
          METHOD: <<METHOD_DELETE>>\
          HEADERS: [<<HEADER_CONTENT_TYPE>>, <<HEADER_ACCEPT>>]\
          BODY: <<BODY_EMPTY>>\
\