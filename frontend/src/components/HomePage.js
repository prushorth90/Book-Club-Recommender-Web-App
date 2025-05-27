import React, { useState } from "react";
import {Container, Grid, Button} from '@material-ui/core';
import { useNavigate } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Title3 from "./clubDisplayHelpers/Title3";

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


function HomePage(){

    const navigate = useNavigate();
	const classes = useStyles();

    const handleLogin = async (e) => {
        navigate('/login/');
    }

    const handleSignup = async (e) => {
        navigate('/signup/');
    }

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
                    <Title3 style={{marginTop: '100px'}}>
                        Bookaholics
                    </Title3>
                    <Grid sx={{
                            display: 'flex',
                            flexDirection: 'row',
                        }}>

						<Button
							type="submit"
							fullWidth
							variant="contained"
							color="primary"
                            onClick={handleLogin}
							style={{backgroundColor: '#643513', marginTop: '20px'}}
						>
							Login
						</Button>

						<Button
							type="submit"
							fullWidth
							variant="contained"
							color="primary"
                            onClick={handleSignup}
							style={{backgroundColor: '#643513', marginTop: '20px'}}
						>
							Sign Up
						</Button>
                    </Grid>
                </div>
		    </Container>
        </div>
            
        </>);
};

export default HomePage;