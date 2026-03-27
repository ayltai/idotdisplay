import { Divider, message, Segmented, Switch, Typography, } from 'antd';
import { useState, } from 'react';
import { useTranslation, } from 'react-i18next';

import { BASE_URL, } from './constants';

export const Controls = () => {
    const [ messageApi, contextHolder, ] = message.useMessage();

    const { t, } = useTranslation();

    const [ power,   setPower,   ] = useState(true);
    const [ display, setDisplay, ] = useState(t('label.display.random'));

    const handlePowerChange = async (checked : boolean) => {
        try {
            const response = await fetch(`${BASE_URL}/api/v1/power/${checked ? 'on' : 'off'}`, {
                method : 'POST',
            });

            if (response.ok) {
                setPower(checked);
            } else {
                messageApi.open({
                    type     : 'error',
                    duration : 5,
                    content  : response.statusText,
                });
            }
        } catch (error) {
            messageApi.open({
                type     : 'error',
                duration : 5,
                content  : (error as Error).message,
            });
        }
    };

    const handleDisplayChange = async (value : string) => {
        try {
            const response = await fetch(`${BASE_URL}/api/v1/${value.toLowerCase()}`, {
                method : 'POST',
            });

            if (response.ok) {
                setDisplay(value);
            } else {
                messageApi.open({
                    type    : 'error',
                    content : response.statusText,
                });
            }
        } catch (error) {
            messageApi.open({
                type    : 'error',
                content : (error as Error).message,
            });
        }
    };

    return (
        <div style={{
            margin : 8,
        }}>
            {contextHolder}
            <div style={{
                width      : '100%',
                padding    : 8,
                gap        : 16,
                display    : 'flex',
                alignItems : 'center',
            }}>
                <Typography.Text style={{
                    flex : 1,
                }}>
                    {t('label.power')}
                </Typography.Text>
                <Switch
                    style={{
                        margin : 8,
                    }}
                    value={power}
                    onChange={handlePowerChange} />
            </div>
            <Divider />
            <div style={{
                margin : 8,
            }}>
                <Typography.Text style={{
                    flex : 1,
                }}>
                    {t('label.display')}
                </Typography.Text>
            </div>
            <div>
                <Segmented<string>
                    style={{
                        margin : 8,
                    }}
                    options={[
                        t('label.display.random'),
                        t('label.display.clock'),
                        t('label.display.artwork'),
                        t('label.display.landmarks'),
                        t('label.display.seasons'),
                        t('label.display.celebrities'),
                        t('label.display.games'),
                    ]}
                    value={display}
                    onChange={handleDisplayChange} />
            </div>
        </div>
    );
};
