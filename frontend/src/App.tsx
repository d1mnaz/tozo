import { Helmet, HelmetProvider } from "react-19-helmet-async";
import Container from "@mui/material/Container";
import { AuthContextProvider } from "./AuthContext";
import ThemeProvider from "./ThemeProvider";
import Router from "./Router";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

function App() {
  return (
    <>
      <AuthContextProvider>
        <HelmetProvider>
          <Helmet>
            <title>Tozo</title>
          </Helmet>
          <ThemeProvider>
            <Container maxWidth="md">
              <Router />
              <h1>Vite + React</h1>
            </Container>
          </ThemeProvider>
        </HelmetProvider>
      </AuthContextProvider>
    </>
  );
}

export default App;
