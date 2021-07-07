document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#ind-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // When user submits form, get the form data
  document.querySelector('#compose-form').onsubmit = function() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    //Testing - this worked...I am getting the form data
    //console.log(`${recipients} ${subject} ${body}`)

    // Use the form data to make an API POST content of form to an email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result)
    })
    //Need to put the as a .then so it waits to the email is sent before loading
    .then(load_mailbox('sent'));    

    // So the form doesn't actually resubmit the page request
    return false;
  }

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#ind-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the emails for the requested mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    //For testing
    console.log(emails);

    // For each email in response...create a div and display contents in that div
    emails.forEach(function(email) {
      const id = email.id;
      var box = document.createElement('div');
      // if email is read make background of div gray
      if (email.read) {
        box.style.backgroundColor = "lightgray";
      };
      box.classList.add('email-div');
      box.innerHTML = `<b>${email.sender}</b> ${email.subject} <i>${email.timestamp}</i>`;
      box.addEventListener('click', email => {
        // This is working to send the email's id to my new function below
        get_email(id);
      });
      document.querySelector('#emails-view').append(box);
    });
  });

  
}
  
function get_email(email_id) {
    // Show the email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#ind-email-view').style.display = 'block';

    // clear out the HTML of the ind-email-view div 
    document.querySelector('#ind-email-view').innerHTML = '';

    // Make API call to get the email details
    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Mark email as read
      fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
          })
      });

      // Add all the email details to the view-div
      document.querySelector('#ind-email-view').innerHTML += `<b>From: </b>${email.sender}<br>`;
      document.querySelector('#ind-email-view').innerHTML += `<b>To: </b>${email.recipients}<br>`;
      document.querySelector('#ind-email-view').innerHTML += `<b>Subject: </b>${email.subject}<br>`;
      document.querySelector('#ind-email-view').innerHTML += `<b>Timestamp: </b>${email.timestamp}<br><hr>`;

      // Create reply button
      var reply = document.createElement('button');
      reply.innerHTML = "Reply";
      document.querySelector('#ind-email-view').appendChild(reply);
      reply.addEventListener('click', () => {
        console.log('button clicked');
      });
      // display email body
      document.querySelector('#ind-email-view').innerHTML += `<br><br>${email.body}<br><br>`;

// For the two ifs below...need to add in "and if user is not the sender"
      // Check if I can get the request.user in the console
      //Try getting the user id
      var user = document.querySelector('#user').innerHTML;
      console.log(user);
      // Only show the archive buttons below if the user is not the sender
      if (user !== email.sender) {

        // Create button to archive emails if not already archived
        if (email.archived === false) {
        var archive = document.createElement('button');
        archive.innerHTML = "Archive";
        document.querySelector('#ind-email-view').appendChild(archive)
        archive.addEventListener('click', () => {
          archive_email(email);     
        });
        };
      
        // Create button to unarchive emails if they're archived
        if (email.archived === true) {
        var unarchive = document.createElement('button');
        unarchive.innerHTML = "Unarchive";
        document.querySelector('#ind-email-view').appendChild(unarchive)
        unarchive.addEventListener('click', () => {
          unarchive_email(email);     
        });
        };
      };
      
    });

    
}

function archive_email(email) {
  // Use API to archive email
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
     })
  })
  .then(load_mailbox('inbox'))
  
}

function unarchive_email(email) {
  // Use API to archive email
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
     })
  })
  .then(load_mailbox('inbox'))
  
}

function email_reply(email){
    console.log('button clicked')
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#ind-email-view').style.display = 'none';

    // Pre-fill to: input with the email sender

}
  // For testing...the line below would add to the html...the 2nd line woudl replace the html
  //document.querySelector('#emails-view').append("Testing");
  //" "('#emails-view').innerHTML = "Testing"
