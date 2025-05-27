import React from 'react'
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Navigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';
import { useContext } from 'react';


const PrivateRoute2 = ({children, ...rest }) => {
    let {user} = useContext(AuthContext)


    return user ? <Navigate to="/dashboard" /> :   children

};

export default PrivateRoute2;