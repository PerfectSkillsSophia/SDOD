// function validateInput(event) {
//     const inputValue = event.target.value;
//     const firstCharacter = inputValue.charAt(0);

//     // Remove spaces
//     event.target.value = inputValue.replace(/\s/g, '');

//     // Check for special characters or numbers at the beginning
//     const regex = /^[^A-Za-z]/;
//     if (regex.test(firstCharacter)) {
//       event.target.value = '';
//     }
//   }


// function validateInput(event) {
//     const inputValue = event.target.value;

//     // Remove spaces and replace with underscores
//     const sanitizedValue = inputValue.replace(/\s+/g, '_');
    
//     // Check for special characters or numbers at the beginning
//     const regex = /^[A-Za-z_]/;
//     if (!regex.test(sanitizedValue)) {
//         event.target.value = '';
//     } else {
//         event.target.value = sanitizedValue;
//     }
// }

function validateInput(event) {
    const inputValue = event.target.value;

    // Remove spaces and replace with underscores
    const sanitizedValue = inputValue.replace(/\s+/g, '_');
    
    // Check for characters that are not allowed (non-alphabetic, non-underscore, non-numeric)
    const regex = /[^A-Za-z0-9_]/g;
    if (regex.test(sanitizedValue)) {
        const validCharacters = sanitizedValue.replace(regex, '');
        event.target.value = validCharacters;
    } else {
        event.target.value = sanitizedValue;
    }
}

