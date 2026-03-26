import { browserTracingIntegration, ErrorBoundary, init, replayIntegration, } from '@sentry/react';
import { Alert, } from 'antd';
import { StrictMode, Suspense, } from 'react';
import { createRoot, } from 'react-dom/client';

import { App, } from './App';

if (import.meta.env.VITE_APP_SENTRY_API_KEY) init({
    dsn          : import.meta.env.VITE_APP_SENTRY_API_KEY,
    integrations : [
        browserTracingIntegration(),
        replayIntegration(),
    ],
});

const Root = () => (
    <StrictMode>
        <Suspense fallback='Loading'>
            <ErrorBoundary fallback={<Alert.ErrorBoundary />}>
                <App />
            </ErrorBoundary>
        </Suspense>
    </StrictMode>
);

createRoot(document.getElementById('root')!).render(<Root />);
