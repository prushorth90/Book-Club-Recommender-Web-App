import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../axios';
//MaterialUI
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
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

export default function Create() {
	const navigate = useNavigate();

	const initialFormData = Object.freeze({
		old_password: '',
		new_password: ''
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

		axiosInstance.put('change-password/', {
			old_password: formData.old_password,
			new_password: formData.new_password
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
					Update Password
				</Typography>
				<form className={classes.form} noValidate>
					<Grid container spacing={2}>
						<Grid item xs={12}>
						<TextField
								variant="outlined"
								required
								fullWidth
								id="old_password"
								label="Old Password"
								name="old_password"
								type="password"
								autoComplete="old_password"
								value={formData.old_password}
								onChange={handleChange}
							/>
						</Grid>
						
                        <Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="new_password"
								label="New Password"
								name="new_password"
								type="password"
								autoComplete="new_password"
								value={formData.new_password}
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