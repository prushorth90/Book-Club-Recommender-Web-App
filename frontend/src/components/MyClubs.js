import React, { useEffect, useState } from "react";
import { makeStyles, Container, Grid} from "@material-ui/core";
import { useParams} from "react-router-dom";
import axiosInstance from '../axios';

import MyClubsInfo from "./myClubsListHelpers/MyClubsInfo";
import MyClubsInfoLoadingComponent from "./myClubsListHelpers/MyClubsInfoLoading";
import Template from './Template';
import Title from './clubDisplayHelpers/Title';
import Parragraph from './clubDisplayHelpers/Parragraph';
import UserRecommenderList from './userRecommenderHelpers/UserRecommenderList';

const useStyles = makeStyles((theme) => ({
    container:{
        paddingTop: theme.spacing(10),
        overflow:"auto",
        maxHeight: 800,
        backgroundColor: '#f5f5f5',
        minWidth: '100%',
        minHeight: '100%',
    }
}));

const MyClubs = () => {

    const { club } = useParams();
    const MyClubsInfoLoading = MyClubsInfoLoadingComponent(MyClubsInfo);
    const [appState, setAppState] = useState({
        loading: false,
        clubs: null,
    });

    useEffect(() => {
        setAppState({ loading: true });
        axiosInstance.get('my-clubs-list/').then((res) => {
            setAppState({ clubs: res.data, loading: false });
            console.log(res.data);
        });
    }, [setAppState]);

    const classes = useStyles();
    return (
        <Container className ={classes.container}>
            <Template/>
            <Grid container>
                <Grid item sm={1} >
                </Grid>
                <Grid item sm={6} >
                    <Title>My Clubs</Title>

                    <Parragraph>This is a list with all of your Clubs</Parragraph>
                    <MyClubsInfoLoading isLoading={appState.loading} clubs={appState.clubs} />
                </Grid>
                <Grid item sm={4}>
                    <UserRecommenderList/>
                </Grid>
            </Grid>
        </Container>
    )
};

export default MyClubs;
