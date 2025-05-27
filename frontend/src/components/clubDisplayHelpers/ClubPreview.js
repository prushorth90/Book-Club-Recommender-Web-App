import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Card from '@material-ui/core/Card';
import ClubDescription from './ClubDescription';
import PostList from './PostList';
import Template from '../Template';
import CardMedia from '@mui/material/CardMedia';



const mdTheme = createTheme();

export default function ClubPreview() {

  return (
    <>
    <Template/>
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              {/* Club description */}
              <Grid item xs={12}>
                <Card>
                  <Grid sx={{
                        display: 'flex',
                        flexDirection: 'row',
                      }}>
                    <CardMedia
                      component="img"
                      sx={{ width: 240 }}
                      image="https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?cs=srgb&dl=pexels-janko-ferlic-590493.jpg&fm=jpg"
                    />
                    <Container
                      sx={{
                        p: 2,
                        display: 'flex',
                        flexDirection: 'column',
                      }}
                    >
                      <ClubDescription />
                    </Container>
                  </Grid>
                </Card>
              </Grid>
              {/* Post */}
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                  <PostList/>
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
    </>
  );
}
