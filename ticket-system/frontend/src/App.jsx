import { useState } from 'react'
import Login from './Login'
import Register from './Register'
import CreateTicket from './CreateTicket'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  return (
    <div className="app">
      <Register />
      {isLoggedIn ? (
        <>
          <p>Logged in</p>
          <CreateTicket />
        </>
      ) : (
        <Login onLoginSuccess={() => setIsLoggedIn(true)} />
      )}
    </div>
  )
}

export default App