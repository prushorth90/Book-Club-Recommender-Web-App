import React from 'react'
import Intro from './intro/Intro';
import About from './about/About';
import ProductList from "./productList/ProductList";
import {BrowserRouter as Router} from 'react-router-dom';
import { ThemeContext } from "./context";

const Home = () => {
  return (
    <div>
        <Intro/>
        <About/>
        <ProductList />
    </div>
);
}

export default Home