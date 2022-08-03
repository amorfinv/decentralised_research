<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" minScale="1e+08" version="3.24.1-Tisler" styleCategories="AllStyleCategories" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" fetchMode="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="bool" value="false" name="WMSBackgroundLayer"/>
      <Option type="bool" value="false" name="WMSPublishDataSourceUrl"/>
      <Option type="int" value="0" name="embeddedWidgets/count"/>
      <Option type="QString" value="Value" name="identify/format"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" value="" name="name"/>
      <Option name="properties"/>
      <Option type="QString" value="collection" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer classificationMax="500" band="1" nodataColor="" opacity="1" type="singlebandpseudocolor" alphaBand="-1" classificationMin="0">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader maximumValue="500" minimumValue="0" labelPrecision="4" clip="0" colorRampType="INTERPOLATED" classificationMode="1">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" value="68,1,84,191" name="color1"/>
              <Option type="QString" value="253,231,37,191" name="color2"/>
              <Option type="QString" value="ccw" name="direction"/>
              <Option type="QString" value="0" name="discrete"/>
              <Option type="QString" value="gradient" name="rampType"/>
              <Option type="QString" value="rgb" name="spec"/>
              <Option type="QString" value="0.0196078;70,8,92,191;rgb;ccw:0.0392157;71,16,99,191;rgb;ccw:0.0588235;72,23,105,191;rgb;ccw:0.0784314;72,29,111,191;rgb;ccw:0.0980392;72,36,117,191;rgb;ccw:0.117647;71,42,122,191;rgb;ccw:0.137255;70,48,126,191;rgb;ccw:0.156863;69,55,129,191;rgb;ccw:0.176471;67,61,132,191;rgb;ccw:0.196078;65,66,135,191;rgb;ccw:0.215686;63,72,137,191;rgb;ccw:0.235294;61,78,138,191;rgb;ccw:0.254902;58,83,139,191;rgb;ccw:0.27451;56,89,140,191;rgb;ccw:0.294118;53,94,141,191;rgb;ccw:0.313725;51,99,141,191;rgb;ccw:0.333333;49,104,142,191;rgb;ccw:0.352941;46,109,142,191;rgb;ccw:0.372549;44,113,142,191;rgb;ccw:0.392157;42,118,142,191;rgb;ccw:0.411765;41,123,142,191;rgb;ccw:0.431373;39,128,142,191;rgb;ccw:0.45098;37,132,142,191;rgb;ccw:0.470588;35,137,142,191;rgb;ccw:0.490196;33,142,141,191;rgb;ccw:0.509804;32,146,140,191;rgb;ccw:0.529412;31,151,139,191;rgb;ccw:0.54902;30,156,137,191;rgb;ccw:0.568627;31,161,136,191;rgb;ccw:0.588235;33,165,133,191;rgb;ccw:0.607843;36,170,131,191;rgb;ccw:0.627451;40,174,128,191;rgb;ccw:0.647059;46,179,124,191;rgb;ccw:0.666667;53,183,121,191;rgb;ccw:0.686275;61,188,116,191;rgb;ccw:0.705882;70,192,111,191;rgb;ccw:0.72549;80,196,106,191;rgb;ccw:0.745098;90,200,100,191;rgb;ccw:0.764706;101,203,94,191;rgb;ccw:0.784314;112,207,87,191;rgb;ccw:0.803922;124,210,80,191;rgb;ccw:0.823529;137,213,72,191;rgb;ccw:0.843137;149,216,64,191;rgb;ccw:0.862745;162,218,55,191;rgb;ccw:0.882353;176,221,47,191;rgb;ccw:0.901961;189,223,38,191;rgb;ccw:0.921569;202,225,31,191;rgb;ccw:0.941176;216,226,25,191;rgb;ccw:0.960784;229,228,25,191;rgb;ccw:0.980392;241,229,29,191;rgb;ccw" name="stops"/>
            </Option>
            <prop k="color1" v="68,1,84,191"/>
            <prop k="color2" v="253,231,37,191"/>
            <prop k="direction" v="ccw"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="spec" v="rgb"/>
            <prop k="stops" v="0.0196078;70,8,92,191;rgb;ccw:0.0392157;71,16,99,191;rgb;ccw:0.0588235;72,23,105,191;rgb;ccw:0.0784314;72,29,111,191;rgb;ccw:0.0980392;72,36,117,191;rgb;ccw:0.117647;71,42,122,191;rgb;ccw:0.137255;70,48,126,191;rgb;ccw:0.156863;69,55,129,191;rgb;ccw:0.176471;67,61,132,191;rgb;ccw:0.196078;65,66,135,191;rgb;ccw:0.215686;63,72,137,191;rgb;ccw:0.235294;61,78,138,191;rgb;ccw:0.254902;58,83,139,191;rgb;ccw:0.27451;56,89,140,191;rgb;ccw:0.294118;53,94,141,191;rgb;ccw:0.313725;51,99,141,191;rgb;ccw:0.333333;49,104,142,191;rgb;ccw:0.352941;46,109,142,191;rgb;ccw:0.372549;44,113,142,191;rgb;ccw:0.392157;42,118,142,191;rgb;ccw:0.411765;41,123,142,191;rgb;ccw:0.431373;39,128,142,191;rgb;ccw:0.45098;37,132,142,191;rgb;ccw:0.470588;35,137,142,191;rgb;ccw:0.490196;33,142,141,191;rgb;ccw:0.509804;32,146,140,191;rgb;ccw:0.529412;31,151,139,191;rgb;ccw:0.54902;30,156,137,191;rgb;ccw:0.568627;31,161,136,191;rgb;ccw:0.588235;33,165,133,191;rgb;ccw:0.607843;36,170,131,191;rgb;ccw:0.627451;40,174,128,191;rgb;ccw:0.647059;46,179,124,191;rgb;ccw:0.666667;53,183,121,191;rgb;ccw:0.686275;61,188,116,191;rgb;ccw:0.705882;70,192,111,191;rgb;ccw:0.72549;80,196,106,191;rgb;ccw:0.745098;90,200,100,191;rgb;ccw:0.764706;101,203,94,191;rgb;ccw:0.784314;112,207,87,191;rgb;ccw:0.803922;124,210,80,191;rgb;ccw:0.823529;137,213,72,191;rgb;ccw:0.843137;149,216,64,191;rgb;ccw:0.862745;162,218,55,191;rgb;ccw:0.882353;176,221,47,191;rgb;ccw:0.901961;189,223,38,191;rgb;ccw:0.921569;202,225,31,191;rgb;ccw:0.941176;216,226,25,191;rgb;ccw:0.960784;229,228,25,191;rgb;ccw:0.980392;241,229,29,191;rgb;ccw"/>
          </colorramp>
          <item label="0,0000" color="#440154" alpha="191" value="0"/>
          <item label="9,8039" color="#46085c" alpha="191" value="9.8039"/>
          <item label="19,6078" color="#471063" alpha="191" value="19.60785"/>
          <item label="29,4118" color="#481769" alpha="191" value="29.41175"/>
          <item label="39,2157" color="#481d6f" alpha="191" value="39.2157"/>
          <item label="49,0196" color="#482475" alpha="191" value="49.019600000000004"/>
          <item label="58,8235" color="#472a7a" alpha="191" value="58.8235"/>
          <item label="68,6275" color="#46307e" alpha="191" value="68.6275"/>
          <item label="78,4315" color="#453781" alpha="191" value="78.4315"/>
          <item label="88,2355" color="#433d84" alpha="191" value="88.23549999999999"/>
          <item label="98,0390" color="#414287" alpha="191" value="98.039"/>
          <item label="107,8430" color="#3f4889" alpha="191" value="107.84299999999999"/>
          <item label="117,6470" color="#3d4e8a" alpha="191" value="117.647"/>
          <item label="127,4510" color="#3a538b" alpha="191" value="127.45100000000001"/>
          <item label="137,2550" color="#38598c" alpha="191" value="137.255"/>
          <item label="147,0590" color="#355e8d" alpha="191" value="147.059"/>
          <item label="156,8625" color="#33638d" alpha="191" value="156.86249999999998"/>
          <item label="166,6665" color="#31688e" alpha="191" value="166.66649999999998"/>
          <item label="176,4705" color="#2e6d8e" alpha="191" value="176.47050000000002"/>
          <item label="186,2745" color="#2c718e" alpha="191" value="186.27450000000002"/>
          <item label="196,0785" color="#2a768e" alpha="191" value="196.0785"/>
          <item label="205,8825" color="#297b8e" alpha="191" value="205.8825"/>
          <item label="215,6865" color="#27808e" alpha="191" value="215.6865"/>
          <item label="225,4900" color="#25848e" alpha="191" value="225.49"/>
          <item label="235,2940" color="#23898e" alpha="191" value="235.294"/>
          <item label="245,0980" color="#218e8d" alpha="191" value="245.098"/>
          <item label="254,9020" color="#20928c" alpha="191" value="254.90200000000002"/>
          <item label="264,7060" color="#1f978b" alpha="191" value="264.706"/>
          <item label="274,5100" color="#1e9c89" alpha="191" value="274.51"/>
          <item label="284,3135" color="#1fa188" alpha="191" value="284.3135"/>
          <item label="294,1175" color="#21a585" alpha="191" value="294.11749999999995"/>
          <item label="303,9215" color="#24aa83" alpha="191" value="303.92150000000004"/>
          <item label="313,7255" color="#28ae80" alpha="191" value="313.7255"/>
          <item label="323,5295" color="#2eb37c" alpha="191" value="323.52950000000004"/>
          <item label="333,3335" color="#35b779" alpha="191" value="333.3335"/>
          <item label="343,1375" color="#3dbc74" alpha="191" value="343.1375"/>
          <item label="352,9410" color="#46c06f" alpha="191" value="352.94100000000003"/>
          <item label="362,7450" color="#50c46a" alpha="191" value="362.745"/>
          <item label="372,5490" color="#5ac864" alpha="191" value="372.54900000000004"/>
          <item label="382,3530" color="#65cb5e" alpha="191" value="382.353"/>
          <item label="392,1570" color="#70cf57" alpha="191" value="392.157"/>
          <item label="401,9610" color="#7cd250" alpha="191" value="401.961"/>
          <item label="411,7645" color="#89d548" alpha="191" value="411.7645"/>
          <item label="421,5685" color="#95d840" alpha="191" value="421.56850000000003"/>
          <item label="431,3725" color="#a2da37" alpha="191" value="431.3725"/>
          <item label="441,1765" color="#b0dd2f" alpha="191" value="441.17650000000003"/>
          <item label="450,9805" color="#bddf26" alpha="191" value="450.9805"/>
          <item label="460,7845" color="#cae11f" alpha="191" value="460.7845"/>
          <item label="470,5880" color="#d8e219" alpha="191" value="470.588"/>
          <item label="480,3920" color="#e5e419" alpha="191" value="480.392"/>
          <item label="490,1960" color="#f1e51d" alpha="191" value="490.196"/>
          <item label="500,0000" color="#fde725" alpha="191" value="500"/>
          <rampLegendSettings useContinuousLegend="1" maximumLabel="" suffix="" prefix="" direction="0" orientation="1" minimumLabel="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="QChar" value="" name="decimal_separator"/>
                <Option type="int" value="6" name="decimals"/>
                <Option type="int" value="0" name="rounding_type"/>
                <Option type="bool" value="false" name="show_plus"/>
                <Option type="bool" value="true" name="show_thousand_separator"/>
                <Option type="bool" value="false" name="show_trailing_zeros"/>
                <Option type="QChar" value="" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0" gamma="1"/>
    <huesaturation grayscaleMode="0" invertColors="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" colorizeBlue="128" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
