import React, { useEffect, useState } from "react";
import { makeStyles, Container} from "@material-ui/core";
import { useParams } from "react-router-dom";
import PostInfo from "./PostInfo";
import PostInfoLoadingComponent from "./PostInfoLoading";
import Subtitle from './Subtitle';
import axiosInstance from "../../axios";

const useStyles = makeStyles((theme) => ({
    container:{
        overflow:"auto",
    }
}));


const PostList = () => {
    const { id } = useParams();
    const PostInfoLoading = PostInfoLoadingComponent(PostInfo);

     const [appState, setAppState] = useState({
        loading: true,
        posts: null,
    });

   

    useEffect(() => {
        axiosInstance.get('list-club-posts/'+id+'/') .then((posts) => {
                    const allPosts = posts.data
                    setAppState({ loading: false, posts: allPosts });
                });
    }, [setAppState]);

    const classes = useStyles();
    return <Container className ={classes.container}>
        <Subtitle>Posts</Subtitle>
        <PostInfoLoading isLoading={appState.loading} posts={appState.posts} />
        </Container>
};

export default PostList;