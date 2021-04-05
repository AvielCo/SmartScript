import './App.css';
import React from 'react';
import { Home, Login, Register, Profile, Error, Logout } from './pages';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/profile" component={Profile} />
        <Route exact path="/register" component={Register} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/home" component={Home} />
        <Route exact path="/logout" component={Logout} />
        <Route exact path="/" component={Home} />
        <Route component={Error} />
      </Switch>
    </Router>
  );
}
export default App;
