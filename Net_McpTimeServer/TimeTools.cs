using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;
using System.ComponentModel;

[McpServerToolType]
public static class TimeTools
{
    [McpServerTool, Description("Gets the current time")]
    public static string GetCurrentTime()
    {
        return DateTimeOffset.Now.ToString();
    }

    [McpServerTool, Description("Gets time in specific timezone")]
    public static string GetTimeInTimezone(string timezone)
    {
        try
        {
            var tz = TimeZoneInfo.FindSystemTimeZoneById(timezone);
            return TimeZoneInfo.ConvertTime(DateTimeOffset.Now, tz).ToString();
        }
        catch
        {
            return "Invalid timezone specified";
        }
    }
}