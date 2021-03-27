import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, loginState: loggedIn, ...rest }) => (
    <Route {...rest} render={(props) => (
      loggedIn === true
        ? <Component {...props} />
        : <Redirect to='/' />
    )} />
  )

  export default PrivateRoute;