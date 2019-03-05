/* @flow */

import { UPDATE, UPDATE_SETTINGS } from './actions';

import type { UpdateAction, UpdateSettingsAction } from './actions';


type Action =
    | UpdateAction
    | UpdateSettingsAction
;


export type SettingsState = {|
    +runQualityChecks: boolean,
    +forceSuggestions: boolean,
|};

const initialSettings: SettingsState = {
    runQualityChecks: true,
    forceSuggestions: true,
};

function settings(
    state: SettingsState = initialSettings,
    action: Action,
): SettingsState {
    switch (action.type) {
        case UPDATE:
            if (!action.data.settings) {
                return state;
            }
            return {
                runQualityChecks: action.data.settings.quality_checks,
                forceSuggestions: action.data.settings.force_suggestions,
            };
        case UPDATE_SETTINGS:
            return {
                ...state,
                ...action.settings,
            };
        default:
            return state;
    }
}


export type UserState = {|
    +isAuthenticated: boolean,
    +id: string,
    +displayName: string,
    +email: string,
    +username: string,
    +managerForLocales: Array<string>,
    +translatorForLocales: Array<string>,
    +translatorForProjects: Array<string>,
    +settings: SettingsState,
    +preferredLocales: Array<string>,
    +signInURL: string,
    +signOutURL: string,
|};

const initial: UserState = {
    isAuthenticated: false,
    id: '',
    displayName: '',
    email: '',
    username: '',
    managerForLocales: [],
    translatorForLocales: [],
    translatorForProjects: [],
    settings: initialSettings,
    preferredLocales: [],
    signInURL: '',
    signOutURL: '',
};

export default function reducer(
    state: UserState = initial,
    action: Action,
): UserState {
    switch (action.type) {
        case UPDATE:
            return {
                isAuthenticated: action.data.is_authenticated,
                id: action.data.id,
                displayName: action.data.display_name,
                email: action.data.email,
                username: action.data.username,
                managerForLocales: action.data.manager_for_locales,
                translatorForLocales: action.data.translator_for_locales,
                translatorForProjects: action.data.translator_for_projects,
                settings: settings(state.settings, action),
                preferredLocales: action.data.preferred_locales,
                signInURL: action.data.login_url,
                signOutURL: action.data.logout_url,
            };
        case UPDATE_SETTINGS:
            return {
                ...state,
                settings: settings(state.settings, action),
            };
        default:
            return state;
    }
}
