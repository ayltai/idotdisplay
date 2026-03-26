import { App as AntApp, ConfigProvider, theme, } from 'antd';
import { useEffect, useState, } from 'react';

import { Controls, } from './Controls';
import { apply, } from './i18n';
import en from './i18n/en.json';
import { handleError, } from './utils';

export const App = () => {
    const [ i18nInitialized, setI18nInitialized, ] = useState(false);

    useEffect(() => {
        apply({
            language           : navigator.language.substring(0, 2),
            supportedLanguages : [
                'en',
            ],
            fallbackLanguage   : 'en',
            resources          : {
                en : {
                    translation : en,
                },
            },
        }).then(() => setI18nInitialized(true)).catch(handleError);
    }, []);

    if (i18nInitialized) return (
        <ConfigProvider theme={{
            algorithm : theme.darkAlgorithm,
            token     : {
                colorPrimary : '#1890ff',
            },
        }}>
            <AntApp>
                <Controls />
            </AntApp>
        </ConfigProvider>
    );

    return null;
};
