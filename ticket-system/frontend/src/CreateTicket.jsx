import { useState } from 'react';

function CreateTicket() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  async function handleSubmit() {
    const response = await fetch('http://localhost:5000/tickets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title, description: description }),
      credentials: 'include'
    });

    const data = await response.json();
    console.log(data);
  }

  return (
    <div className="create-ticket">
      <h2>Create Ticket</h2>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button onClick={handleSubmit}>Create Ticket</button>
    </div>
  );
}

export default CreateTicket;
