using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace StayHappyWebApp.Controllers
{
  public class PythonController : Controller
  {
    [HttpGet]
    public IActionResult RunPythonScript()
    {
      // Path to the Python executable
      string pythonExe = @"C:\Users\kvist\Skola\AI\djupinlaerning\stay_happy\StayHappyWebApp\.venv\Scripts\python.exe";

      // Path to the Python script
      string script = @"C:\Users\kvist\Skola\AI\djupinlaerning\stay_happy\StayHappyWebApp\Scripts\python\main.py";

      // Create a process to start the Python script
      ProcessStartInfo psi = new ProcessStartInfo();
      psi.FileName = pythonExe;
      psi.Arguments = $"\"{script}\"";  // Arguments for the Python script
      psi.RedirectStandardOutput = true; // Capture output
      psi.UseShellExecute = false; // Don't use shell
      psi.CreateNoWindow = true; // Don't create a window

      string result;

      using (Process process = Process.Start(psi))
      {
        result = process.StandardOutput.ReadToEnd(); // Read the output
        process.WaitForExit();
      }

      // Return the result to the view
      return Content(result);
    }
  }
}
