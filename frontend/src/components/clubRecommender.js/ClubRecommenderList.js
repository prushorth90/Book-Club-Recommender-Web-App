import React, { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core";
import Title from "../clubDisplayHelpers/Title";
import axiosInstance from "../../axios";
import ClubRecommenderInfo from "./ClubRecommenderInfo";
import ClubRecommenderInfoLoadingComponent from "./ClubRecommenderInfoLoading";
import { useParams } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
    container:{
        paddingTop: theme.spacing(10),
        overflow:"auto",
        maxHeight: 800,
    }
}));


const ClubRecommenderList = () => {
    const { id } = useParams();
    const ClubRecommenderInfoLoading = ClubRecommenderInfoLoadingComponent(ClubRecommenderInfo);

     const [appState, setAppState] = useState({
        loading: true,
        recommendations: null,
    });

   

    useEffect(() => {
        axiosInstance.get('club-recommendations/'+id+'/') .then((recommendations) => {
                    const allRecommendations = recommendations.data
                    setAppState({ loading: false, recommendations: allRecommendations });
                });
    }, [setAppState]);

    const classes = useStyles();
    return <div 
    style={{ marginTop: '40px',
    marginLeft: '40px', 
    flexDirection: 'column',
    alignItems: 'center' }} >
    <Title>Book Recommendations</Title>
    <ClubRecommenderInfoLoading isLoading={appState.loading} recommendations={appState.recommendations} />
    </div>
};

export default ClubRecommenderList;