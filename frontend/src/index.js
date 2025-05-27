import App from "./components/App";
import React, { Component } from "react";
import ReactDOM from 'react-dom';
import { ThemeProvider } from "@material-ui/styles"

ReactDOM.render(
    <React.StrictMode>
            <App />
    </React.StrictMode>, 
    document.getElementById('root')
    );