#include <stdio.h>
#include <stdlib.h>

/*
README

My small "library" of functions for working with strings
without using <string.h> and writing them all manually
with addiction of some other functions

Why I made it:
    I was bored in uni on some lectures and this is result 
    of that
    привет Т*****.., очень круто(нет) сидеть 40 минут в тишине в телефоне на паре

Watch out:
    most/all functions which return string were
    memory allocated so they should be freed afterwards. 
    
    Also most of these are super unoptimized and could be
    improved both in speed, memory, readability(not sure here) 
    and safeness(func takes pointer and realloccates it) 
    
*/

size_t str_len(char* str);
char* str_reverse_full(char* str);
char* str_upper(char* str);
char* str_lower(char* str);
char char_upper(char c);
char char_lower(char c);
size_t contains(char* str, char* sub_str);
char* compress(char* str);
char* strip(char* str);
size_t count(char* str, char* sub_str);
char* replace(char* str, char* sub_str, char* new_str, size_t max_amount);
size_t in_arr(size_t* arr, size_t value, size_t arr_len);
char* replace(char* str, char* sub_str, char* new_sub_str, size_t max_amount);

//extra diff
// get_string()
// split()


int main()
{
    char* str = malloc();
    char* sub_str = malloc();
    char* new_sub_str = malloc();
    
    size_t max_amount = 1;

    printf("input: %s\n", str);
    printf("reversed: %s\n", str_reverse_full(str));
    printf("len = %lu\n", str_len(str));
    printf("to_up: %s\n", str_upper(str));
    printf("to_low: %s\n", str_lower(str));
    printf("sub str: %lu\n", contains(str, sub_str));
    printf("compress: %s\n", compress(str));
    printf("strip: %s\n", strip(str));
    printf("count: %lu\n", count(str, sub_str));
    printf("replace: %s\n", replace(str, sub_str, new_sub_str, max_amount));

    //free(str);
    //you thought I would free? Fool! 
    return 0;
}

size_t str_len(char* str) {
    size_t length = 0;
    int k;

    for (k = 0; str[k] != '\0'; k++) {
        length++;
    }
    return length;
}

char* str_reverse_full(char* str) {
    size_t length = str_len(str);
    size_t reversed_index = length - 1;
    int k;

    char* new_str = malloc((length * sizeof(char)) + 1);
    if (new_str == NULL){
        return NULL;
    }

    for (k = 0; k < length; k++) {
        new_str[reversed_index] = str[k];
        reversed_index--;
    }
    new_str[length] = '\0';
    return new_str;
}

char* str_upper(char* str){
    size_t length = str_len(str);
    int index;

    char* new_str = malloc((length * sizeof(char)) + 1);
    if (new_str == NULL){
        return NULL;
    }

    for (index = 0; index < length; index++) {
        new_str[index] = char_upper(str[index]);
    }
    new_str[length] = '\0';
    return new_str;
}

char* str_lower(char* str){
    size_t length = str_len(str);
    int index;

    char* new_str = malloc((length * sizeof(char)) + 1);
    if (new_str == NULL){
        return NULL;
    }

    for (index = 0; index < length; index++) {
        new_str[index] = char_lower(str[index]);
    }
    new_str[length] = '\0';
    return new_str;
}

char char_upper(char c){
    if (c >= 97 && c <= 122) {
        return (char) c - 32;
    }
    return c;
}

char char_lower(char c){
    if (c >= 65 && c <= 90) {
        return (char) c + 32;
    }
    return c;
}    

size_t contains(char* str, char* sub_str){
    size_t c_index = 0;
    size_t j;
    size_t length = str_len(str);
    size_t req_length = str_len(sub_str);
    size_t found_length = 0;

    size_t flag = 0;

    for (j = 0; j < length; j++){
        if (str[j] == sub_str[0] && !flag){
            flag = 1;
            found_length++;
            continue;
        }

        if (!flag) {
            continue;
        }

        if (found_length == req_length){
            return 1lu;
        }

        if (str[j] == sub_str[found_length]) {
            found_length++;
            continue;
        }
        else{
            found_length = 0;
            continue;
        }
    }
    return 0lu;
}

char* compress(char* str){
    size_t length = str_len(str);
    size_t j;
    size_t k = 0;
    char* new_str = malloc(sizeof(char) * length + 1);
    if (new_str == NULL){
        return NULL;
    }

    for (j = 0; j < length; j++){
        if (str[j] == ' '){
            continue;
        }
        else{
            new_str[k] = str[j];
            k++;
        }
    }
    new_str[k] = '\0';
    return new_str;
}

char* strip(char* str){
    size_t start = 0;
    size_t length = str_len(str);
    char* new_str = malloc((sizeof(char) * length) + 1);
    if (new_str == NULL){
        return NULL;
    }
    //remove them fuckers
    for (size_t j = (length - 1); j > 0; j--){
        if (str[j] != ' '){
            break;
        }
        length--;
    }

    for (size_t j = 0; j < length; j++){
        if (str[j] != ' '){
            start = j;
            break;
        }
    }

    for (size_t j = start; j < length; j++){
        new_str[j - start] = str[j];
    }
    new_str[length - start] = '\0';
    return new_str;
}

size_t count(char* str, char* sub_str){
    size_t length = str_len(str);
    size_t sub_length = str_len(sub_str);
    size_t j = 0;
    size_t result = 0;
    size_t substr_count = 0;

    for (size_t j = 0; j <= (length - sub_length); j++){
        size_t k = 0;
        while (k < sub_length && str[j + k] == sub_str[k]){
            k++;
        }
        if (k == sub_length){
            result++;
        }
    }
    return result;
}

char* replace(char* str, char* sub_str, char* new_sub_str, size_t max_amount){
    //this shit is o(n^2) with bad constant factor :) 
    
    size_t cur_index = 0;
    size_t count_s = count(str, sub_str);
    size_t length = str_len(str);
    size_t sub_length = str_len(sub_str);
    size_t new_sub_str_len = str_len(new_sub_str);
    printf("%zu", count_s);
    
    size_t arr[count_s];
    
    for (size_t j = 0; j <= (length - sub_length); j++){
        size_t k = 0;
        while (k < sub_length && str[j + k] == sub_str[k]) {
            k++;
        }
        if (k == sub_length) {
            arr[cur_index++] = j;
        }
    }
    
    
    
    for (size_t j = 0; j < count_s; j++) {
        //replace 
        printf("j-%zu\n", arr[j]);
    }
    
    size_t new_len = length - ((sub_length - new_sub_str_len)*count_s);
    char* new_str = malloc(sizeof(char) * ((new_len) + 1));
    if (new_str == NULL) {
        return NULL;
    }
    
    size_t check;
    if (max_amount == 0) {
        check = 1LU << 31;
    }
    else if (max_amount > 0) {
        check = max_amount;
    }

    size_t new_str_index = 0;
    for (size_t j = 0; j < length; j++) {
        if ((in_arr(arr, j, count_s)) && (check > 0)) {
            for (size_t i = 0; i < new_sub_str_len; i++) {
                new_str[new_str_index++] = new_sub_str[i];
                j++;
            }
            check--;
        }
        else {
            new_str[new_str_index++] = str[j];
        }
    }
    new_str[new_str_index] = '\0';
    
    return new_str;
}    
    /*
    abobcbobv
    sub = bob
    index 1 (+2) 5 +2
    
    
    
    */
    
    
    //O factor
    // count = O(n)
    /*
    strlen = n
    count = strlen + O(n * k)
    replace = 2 * strlen + count + O(fuck
    
    
    */

char* reverse_only_words(char* str){
    //TODO
}

char* split(char* str, char* splitter){
    //TODO
}

size_t in_arr(size_t* arr, size_t value, size_t arr_len){
    for (size_t j = 0; j < arr_len; j++) {
        if (value == arr[j]) {
            return 1;
        }
    }
    return 0;
}