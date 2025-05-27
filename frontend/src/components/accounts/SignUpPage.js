import React, { useState } from 'react';
import axiosInstance from '../../axios';

import { useNavigate } from 'react-router-dom';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import Title2 from "../clubDisplayHelpers/Title2";
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';


const useStyles = makeStyles((theme) => ({
	paper: {
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
	},
	avatar: {
		margin: theme.spacing(2),
		backgroundColor: '#643513',
	},
	form: {
		width: '100%', // Fix IE 11 issue.
		marginTop: theme.spacing(3),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
}));

export default function SignUpPage() {

	const navigate = useNavigate();
	const initialFormData = Object.freeze({
		first_name: '',
		last_name: '',
		username: '',
        email: '',
        bio: '',
        password: '',
	});

	const [formData, updateFormData] = useState(initialFormData);

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

		axiosInstance
			.post(`/signup/`, {
                first_name: formData.first_name,
                last_name: formData.last_name,
				username: formData.username,
                email: formData.email,
                bio: formData.bio,
				password: formData.password,
			})
			.then((res) => {
				navigate('/login');
				console.log(res);
				console.log(res.data);
				console.log("done")
			});
	};

	const classes = useStyles();

	return (
	<>
		<div className='image' style={{
			backgroundImage: `url(https://images.pexels.com/photos/694740/pexels-photo-694740.jpeg?cs=srgb&dl=pexels-min-an-694740.jpg&fm=jpg)`,
			margin:0,
			minWidth: '100%',
			minHeight: '100%',
			height: '940px',
			backgroundSize: 'cover',
			backgroundPosition: 'center',
			backgroundFilter: 'brightness(50%)',
			}}>
		<Container component="main" maxWidth='sm' margin='100' >
			<CssBaseline />
			
			<div className={classes.paper}>
			<Card style={{
				marginTop: '50px',
				marginBottom: '50px',
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				padding: '35px',
			}}>
				<Avatar className={classes.avatar}></Avatar>
				<Title2>
					Sign up
				</Title2>
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
								onChange={handleChange}
							/>
						</Grid>
                        <Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="password"
								label="Password"
								name="password"
								type="password"
								autoComplete="current-password"
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
						style={{backgroundColor: '#643513',}}
					>
						Sign Up
					</Button>
					<Grid container justify="flex-end">
						<Grid item>
							<Link href="/login" variant="body2">
								Already have an account? Log in
							</Link>
						</Grid>
					</Grid>
				</form>
			</Card>
			</div>
		</Container>
		</div>
		</>
	);
}