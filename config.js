const dotenv = require('dotenv');

dotenv.config();

/**
 * Each of the environment variables which are required during the "serverless" configuration are put here.
 * The environment variable can be either set in the environment or kept in the ".env" file.
 * The error is thrown when the environment variable is not found.
 */
const envVariables = {
    SECURITY_GROUP_IDS: getEnvVariableValue('SECURITY_GROUP_IDS'),
    SUBNET_IDS: getEnvVariableValue('SUBNET_IDS'),
    POSTGRES_HOST: getEnvVariableValue('POSTGRES_HOST'),
    POSTGRES_PORT: getEnvVariableValue('POSTGRES_PORT'),
    POSTGRES_DB: getEnvVariableValue('POSTGRES_DB'),
    POSTGRES_USER: getEnvVariableValue('POSTGRES_USER'),
    POSTGRES_PASSWORD: getEnvVariableValue('POSTGRES_PASSWORD'),
};

function getEnvVariableValue(variableName) {
    if (variableName in process.env) {
        return process.env[variableName];
    }
    throw new Error(`Missing "${variableName}" environment variable!!!`);
}

/**
 * All the environment variables are exported from this javascript file to be used in "serverless" configuration.
 * [https://serverless.com/framework/docs/providers/aws/guide/variables#reference-variables-in-javascript-files]
 */
module.exports.getEnvs = () => ( envVariables );
