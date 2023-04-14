import logo from './logo.svg';
import './App.css';
import { AppProviders } from './providers/AppProviders'
import { MainPage } from './pages/MainPage'

function App() {
  return (
    <AppProviders>
      <MainPage />
    </AppProviders>
  );
}

export default App;
