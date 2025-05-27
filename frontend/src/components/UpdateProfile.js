import React, { useState, useEffect } from 'react';
import axiosInstance from '../axios';
import { useParams } from 'react-router-dom';
//MaterialUI
import { useNavigate } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Template from './Template';

const useStyles = makeStyles((theme) => ({
	paper: {
		marginTop: theme.spacing(8),
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
	},
	form: {
		width: '100%', // Fix IE 11 issue.
		marginTop: theme.spacing(3),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
}));

export default function UpdateProfile() {
	const { name } = useParams();
	const navigate = useNavigate();
	console.log(name);

	const initialFormData = Object.freeze({
		first_name: '',
		last_name: '',
		username: '',
        email: '',
        bio: '',
	});

	const [formData, updateFormData] = useState(initialFormData);

	useEffect(() => {
		axiosInstance.get('current-user/' ).then((res) => {
			console.log(res);
			updateFormData({
				...formData,
				['first_name']: res.data.first_name,
				['last_name']: res.data.last_name,
				['username']: res.data.username,
				['email']: res.data.email,
				['bio']: res.data.bio,
			});
			console.log(res.data);
		});
	}, [updateFormData]);

	const handleChange = (e) => {
		updateFormData({
			...formData,
			// Trimming any whitespace
			[e.target.name]: e.target.value.trim(),
		});
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log(formData);
		console.log(formData.password);

		axiosInstance.put(`edit-user/` + formData.username + '/', {
			username: formData.username,
			first_name: formData.first_name,
			last_name: formData.last_name,
			email: formData.email,
			bio: formData.bio,
		})
		.then((res) => {
			navigate('/dashboard');
		});
	};

	const classes = useStyles();

	return (
		<>
		<Template/>
		<Container component="main" maxWidth="sm">
			<CssBaseline />
			<div className={classes.paper}>
				<Typography component="h1" variant="h5">
					Edit Info
				</Typography>
				<form className={classes.form} noValidate> 
					<Grid container spacing={2}>
						<Grid item xs={12}>
						<TextField
								variant="outlined"
								required
								fullWidth
								id="first_name"
								label="First Name"
								name="first_name"
								autoComplete="firstname"
								value={formData.first_name}
								onChange={handleChange}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="last_name"
								label="Last Name"
								name="last_name"
								autoComplete="lastname"
								value={formData.last_name}
								onChange={handleChange}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="username"
								label="Username"
								name="username"
								autoComplete="username"
								value={formData.username}
								onChange={handleChange}
							/>
						</Grid>
                        <Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="email"
								label="Email Address"
								name="email"
								autoComplete="email"
								value={formData.email}
								onChange={handleChange}
							/>
						</Grid>
                        <Grid item xs={12}>
							<TextField
								variant="outlined"
								fullWidth
                                multiline
                                rows={4}
								id="bio"
								label="Bio"
								name="bio"
								autoComplete="bio"
								value={formData.bio}
								onChange={handleChange}
							/>
						</Grid>
					</Grid>
					<Button
						type="submit"
						fullWidth
						variant="contained"
						color="primary"
						className={classes.submit}
						onClick={handleSubmit}
					>
						confirm
					</Button>
				</form>
			</div>
		</Container>
		</>
	);
}