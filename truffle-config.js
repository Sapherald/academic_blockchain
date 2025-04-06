module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,  // Default Ganache GUI port
      network_id: "*",
    },
    ganache_cli: {
      host: "127.0.0.1",
      port: 8545,  // Default Ganache CLI port
      network_id: "*",
    }
  },
  compilers: {
    solc: {
      version: "0.8.0",    // Specify the Solidity compiler version
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        }
      }
    }
  }
};