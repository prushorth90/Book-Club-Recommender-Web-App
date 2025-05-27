import React, { useEffect, useState } from "react";
import { makeStyles, Container} from "@material-ui/core";
import Title2 from "../clubDisplayHelpers/Title2";
import axiosInstance from "../../axios";
import UserRecommenderInfo from "./UserRecommenderInfo";
import UserRecommenderInfoLoadingComponent from "./UserRecommenderInfoLoading"

const useStyles = makeStyles((theme) => ({
    container:{
        overflow:"auto",
        maxHeight: 800,
    }
}));


const UserRecommenderList = () => {
    const UserRecommenderInfoLoading = UserRecommenderInfoLoadingComponent(UserRecommenderInfo);

     const [appState, setAppState] = useState({
        loading: true,
        recommendations: null,
    });

   

    useEffect(() => {
        axiosInstance.get('user-recommendations/') .then((recommendations) => {
                    const allRecommendations = recommendations.data
                    setAppState({ loading: false, recommendations: allRecommendations });
                });
    }, [setAppState]);

    const classes = useStyles();
    return (
        <div 
        style={{ marginTop: '40px',
        marginLeft: '40px', 
		flexDirection: 'column',
		alignItems: 'center' }} >
        <Title2>Recommendations</Title2>
        <UserRecommenderInfoLoading isLoading={appState.loading} recommendations={appState.recommendations} />
        </div>
        )
};

export default UserRecommenderList;