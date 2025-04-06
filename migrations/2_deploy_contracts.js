const AcademicRecordSystem = artifacts.require("AcademicRecordSystem");

module.exports = function(deployer) {
  deployer.deploy(AcademicRecordSystem);
};