const loadTPDirect=()=>{
    TPDirect.setupSDK(20428, 'app_LV9etJIVwIlMGxLeJxKaO9NDlbniEXFgPAzyNzKX7sjE0VJXCQGBl5v1WECU', 'sandbox');
    TPDirect.card.setup({
        fields: {
            number: {
                element: '#card-number',
                placeholder: '**** **** **** ****'
            },
            expirationDate: {
                element: '#card-expiration-date',
                placeholder: 'MM / YY'
            },
            ccv: {
                element: '#card-ccv',
                placeholder: 'ccv'
            }
        },
        styles: {
            'input': {
                'color': 'gray'
            },
            'input.ccv': {
                'font-size': '15px'
            },
            'input.expiration-date': {
                'font-size': '15px'
            },
            'input.card-number': {
                'font-size': '15px'
            },
            '.valid': {
                'color': 'black'
            },
            '.invalid': {
                'color': 'red'
            }
        }
    })
};