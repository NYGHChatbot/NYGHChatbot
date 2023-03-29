class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),

        }

        this.state = false;
        this.messages = [];
        this.initalToggle = true;
        this.yes_or_no_state = false;
        this.another_question = false;
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        //keeps chatbot open by default
        chatBox.classList.add('chatbox--active');
        this.toggleState(chatBox);

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }

        if (this.initalToggle == true && this.state) {
            let msg = {name: "Amae", message: "Hello, my name is Amae! I can answer your questions related to COVID-19, Monkeypox and Influenza."};
            this.messages.push(msg);
            this.updateChatText(chatbox);
            this.initalToggle = false;
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        
        const yes_string = "yes";
        const no_string = "no";

        let index_yes = text1.indexOf(yes_string);
        let index_no = text1.indexOf(no_string);
        let text_response = "";

        if (this.yes_or_no_state == true) {
            this.yes_or_no_state = false;

            if (index_yes != -1) {
                this.another_question = true;
                text_response = "Great! Is there anything else I can help you with?";
            } 
            else if (index_no != -1) {
                text_response = "Ok. You can either ask your question again to me or contact NYGH's Pharmacy at (416)-756-6666 or NYGHPharmacy@nygh.on.ca";
            }
             
            let msg = {name: "Amae", message: text_response};
            this.messages.push(msg);
            this.updateChatText(chatbox);
            textField.value = ''
        } 
        else if (this.another_question == true) {
            this.another_question = false
            
            if (index_no != -1) {
                text_response = "Ok. See you later!";
            }
             
            let msg = {name: "Amae", message: text_response};
            this.messages.push(msg);
            this.updateChatText(chatbox);
            textField.value = ''
        }
        else {
            //'http://127.0.0.1:5000/predict'
            fetch($SCRIPT_ROOT + '/predict', {
                method: 'POST',
                body: JSON.stringify({ message: text1 }),
                mode: 'cors',
                headers: {
                'Content-Type': 'application/json'
                },
            })
            .then(r => r.json())
            .then(r => {
                let msg2 = { name: "Amae", message: r.answer };
                this.messages.push(msg2);
                if (r.add_message == true) {
                    let add_message = { name: "Amae", message:"Did I answer your question correctly?" };
                    this.messages.push(add_message);
                    this.yes_or_no_state = true;
                }
                this.updateChatText(chatbox)
                textField.value = ''

            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });
        }
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name == "Amae")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

        const chatWindow = document.getElementById('chatbox__messages');
        var xH = chatWindow.scrollHeight;
        chatWindow.scrollTo(0, xH);
    }
}

const chatbox = new Chatbox();
chatbox.display();
