const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="acknowledge-section">
        <h2>Acknowledgement</h2>
        <br></br>
        <p>Humane-AI Net (European project ….)</p>
        <p>AI Builder …</p>
        <p>placeholder</p>
      </div>
      <div className="bug-report-section">
        <h2>Bug Report</h2>
        <br></br>
        <p>Report bugs to: <a href="mailto:bugs@example.com">xxx.yyy@aalto.fi</a></p>
      </div>
      <div className="terms-section">
        <h2>Terms of Service</h2>
        <br></br>
        <p>Read our <a href="/#">Terms of Service</a></p>
      </div>
      <div className="logo-section">
        <img src="./image1.png" alt="Project Logo" />
      </div>
    </footer>
  );
}

export default Footer;