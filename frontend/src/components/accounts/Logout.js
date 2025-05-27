import React, { useEffect, useContext } from 'react';
import axiosInstance from '../../axios';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';


export default function Logout() {
	let {setAuthTokens, setUser, authTokens} = useContext(AuthContext);
	const navigate = useNavigate();

	useEffect(() => {
		const response = axiosInstance.post('logout/blacklist/', {
			refresh_token: localStorage.getItem('refresh_token'),
		});
		setAuthTokens(null);
		setUser(null);
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		axiosInstance.defaults.headers['Authorization'] = null;
		navigate('/');
	});
	return <div>Logout</div>;
}