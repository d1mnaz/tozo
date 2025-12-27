import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ToastContextProvider } from "./ToastContext";
import { Helmet, HelmetProvider } from "react-19-helmet-async";
import Container from "@mui/material/Container";
import { AuthContextProvider } from "./AuthContext";
import ThemeProvider from "./ThemeProvider";
import Router from "./Router";
import Toasts from "./components/Toasts";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

const queryClient = new QueryClient();

function App() {
  return (
    <>
      <QueryClientProvider client={queryClient}>
        <AuthContextProvider>
          <HelmetProvider>
            <Helmet>
              <title>Tozo</title>
            </Helmet>
            <ThemeProvider>
              <ToastContextProvider>
                <Container maxWidth="md">
                  <Toasts />
                  <Router />
                  <h1>Vite + React</h1>
                </Container>
              </ToastContextProvider>
            </ThemeProvider>
          </HelmetProvider>
        </AuthContextProvider>
      </QueryClientProvider>
    </>
  );
}

export default App;
