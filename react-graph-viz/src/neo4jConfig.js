/**
 * Single source for Neo4j Aura settings. Keep in sync with Cred/Neo4j-fb691b6b-Created-2026-05-06.txt
 *
 * If you see "authentication failure": open https://console.neo4j.io → your instance →
 * reset the password, paste it here (and in Cred), rebuild/redeploy.
 *
 * CRA only embeds REACT_APP_* at build time; NEO4J_* without prefix is usually undefined in the browser.
 */

const DEFAULTS = {
  uri: 'neo4j+s://fb691b6b.databases.neo4j.io',
  user: 'neo4j',
  password: 'UfdsQn6_jKzgFzp0c9iFgtJ0PP6-zYkJJO-cR6TUpws',
  database: 'neo4j',
};

function pickEnv(...candidates) {
  for (const v of candidates) {
    if (v == null) continue;
    const s = String(v).trim();
    if (s === '' || s === 'undefined') continue;
    return s;
  }
  return undefined;
}

export function getNeo4jConfig() {
  return {
    uri:
      pickEnv(
        process.env.REACT_APP_NEO4J_URI,
        process.env.NEO4J_URI
      ) || DEFAULTS.uri,
    user:
      pickEnv(
        process.env.REACT_APP_NEO4J_USERNAME,
        process.env.REACT_APP_NEO4J_USER,
        process.env.NEO4J_USERNAME,
        process.env.NEO4J_USER
      ) || DEFAULTS.user,
    password:
      pickEnv(
        process.env.REACT_APP_NEO4J_PASSWORD,
        process.env.NEO4J_PASSWORD
      ) || DEFAULTS.password,
    database:
      pickEnv(
        process.env.REACT_APP_NEO4J_DATABASE,
        process.env.NEO4J_DATABASE
      ) || DEFAULTS.database,
  };
}
